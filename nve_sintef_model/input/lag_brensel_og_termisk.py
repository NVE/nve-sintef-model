import os
import pandas as pd

# TODO: dette skriptet bør på sikt flyttes til nve_modell, og også de to importene under:
from .emps_script_lag_prefdat import skriv_lag_prefdat_script
from .emps_script_slett_prefdat import skriv_slett_prefdat_script


from nve_modell.sintef.utils.filesystem import lag_output_mappe
from nve_modell.sintef.utils.type_check import (get_path_from_dict,
                                                get_type_from_dict)

from nve_modell.thema.io.plants import (get_input_plant_capacities_df,
                                        get_input_plant_profiles_df,
                                        get_input_plant_profile_scen_df)

# hent modifisert funksjon som fungerer for v2.4
from nve_modell.thema.io.plants_la2020 import get_input_plants_df

from nve_modell.thema.io.fuels import (get_input_fuels_df,
                                       get_input_fuel_price_profiles_df,
                                       get_input_fuel_prices_df)

from nve_modell.thema.io.hours import get_input_hours_df

from nve_modell.prosjekt.la.brensel_og_termisk.les_ekstra_brensel_df      import les_ekstra_brensel_df
from nve_modell.prosjekt.la.brensel_og_termisk.les_fuel_id_brenselnavn_df import les_fuel_id_brenselnavn_df
from nve_modell.prosjekt.la.brensel_og_termisk.les_omr_plant_df           import les_omr_plant_df
from nve_modell.prosjekt.la.brensel_og_termisk.les_scenario_df            import les_scenario_df
from nve_modell.prosjekt.la.brensel_og_termisk.les_slett_pref_df          import les_slett_pref_df

from nve_modell.prosjekt.la.brensel_og_termisk.get_brensel_df           import get_brensel_df
from nve_modell.prosjekt.la.brensel_og_termisk.get_termisk_df           import get_termisk_df
from nve_modell.prosjekt.la.brensel_og_termisk.get_kapasitet_map        import get_kapasitet_map
from nve_modell.prosjekt.la.brensel_og_termisk.get_brenselpris_map      import get_brenselpris_map
from nve_modell.prosjekt.la.brensel_og_termisk.skriv_brenselarkiv_filer import skriv_brenselarkiv_filer


class LagBrenselOgTermisk(object):

    def __init__(self, conf):

        """
        Lager emps-filer basert paa thema-scenarioer
          - emps-filene som lages er 
                brenselprisarkiv (default filnavn 'BRENSEL.ARCH')
                enmdat-script som legger inn thema-plants som pref-varme-kontrakter (default filnavn 'lag_pref.script')
                enmdat-script som sletter pref-kontrakter i emps-omraader (default filnavn 'slett_pref.script')

          - hvilke thema-scenarioer som skal brukes defineres i en excel-fil (med sti conf['path_xlsx_scenarioer'])

          - hvilke sammenhengen mellom thema-plants og emps-omraader defineres i en excel-fil (med sti conf['path_xlsx_omr_plant'])

        hva gjor rutinen
        - lager nye pref-kontrakter for temisk produksjon
          og lager nye brenselsprisarkiv-filer basert paa thema-modellen 
        
        - legger til eventuelle ekstra brensler
        
        - splitter plants i thema inn i fleksibel 
          og mustrun (plants som har min_profile eller fixed_profile)

        grunnen til at disse gjores i samme rutine er at de henger sammen
          - maa lese termiske verk for aa finne ut hvilke brensler som maa med

          - man maa lage ordnet liste med brensler (til arkiv-filene) for aa vite
            hvilket brenselnr hvert brensel har. naar man skal legge inn pref-kontrakter 
            maa brenselsnr gis som input til enmdat-programmet for aa koble pref-kontrakten
            til riktig brensel i brenselsarkivet
        """

        # TODO: bedre doc
        # TODO: verifiser input
        # TODO: unngaa negative priser
        # TODO: avregn??

        self.path_output                = get_path_from_dict(conf, "path_output")
        self.exist_ok                   = False

        self.filversjon                 = 1
        self.brenselavgift              = 0
        self.energi_koef                = 1
        self.navn_brenselarkiv_fil      = "BRENSEL.ARCH"
        self.kommentar_header           = "** filversjon, antall_brensler, sluttuke"
        self.kommentar_brensel          = "** brenselnavn, co2_cont, energi_koef"
        self.kommentar_uke              = "** sluttuke, brenselpris, brenselavgift, co2_pris"

        self.tilgjengelighet_pref       = 100
        self.effektprofil_pref          = 1
        self.slett_pref_dict            = get_type_from_dict(conf, 'slett_pref_dict', (dict))
        self.filnavn_lag_pref_script    = get_type_from_dict(conf, "filnavn_lag_pref_script", (str))
        self.filnavn_slett_pref_script  = get_type_from_dict(conf, "filnavn_slett_pref_script", (str))
        self.prefnr_start               = 100 # -> forste prefnr = 101

        self.min_brenselpris_ore_kwh    = 0.5
        self.min_co2pris_ore_kwh        = 0.0

        self.path_thema_input_dir       = get_path_from_dict(conf, "path_thema_input_dir")
        self.path_xlsx_ekstra_brensler  = get_path_from_dict(conf, "path_xlsx_ekstra_brensler")
        self.path_xlsx_fuel_id_navn     = get_path_from_dict(conf, "path_xlsx_fuel_id_navn")
        self.path_xlsx_omr_plant        = get_path_from_dict(conf, "path_xlsx_omr_plant")

        self.modaar                     = get_type_from_dict(conf, 'modaar', (str))
        self.modaar_id                  = get_type_from_dict(conf, 'modaar_id', (int))
        self.modaar_df                  = pd.DataFrame([[self.modaar_id, f'{self.modaar}', f'{self.modaar}']], columns = ['year_id', 'year_name', 'scenarionavn'])
        self.eurnok                     = get_type_from_dict(conf, "eurnok", (int,float))
        self.antall_aar_data            = get_type_from_dict(conf, "antall_aar_data", int)

        self.sluttuke                   = self.antall_aar_data * 52

        # stier til thema-input-filer
        self.path_hours                 = os.path.join(self.path_thema_input_dir, "Hours.csv")
        self.path_plant_profiles        = os.path.join(self.path_thema_input_dir, "Plant_Profiles.csv")
        self.path_plant_capacities      = os.path.join(self.path_thema_input_dir, "Plant_Capacities.csv")
        self.path_plants                = os.path.join(self.path_thema_input_dir, "Plants.csv")
        self.path_plant_profile_scen    = os.path.join(self.path_thema_input_dir, "Plant_Profile_Scen.csv")
        self.path_fuels                 = os.path.join(self.path_thema_input_dir, "Fuels.csv")
        self.path_fuel_price_profiles   = os.path.join(self.path_thema_input_dir, "Fuel_Price_Profiles.csv")
        self.path_fuel_prices           = os.path.join(self.path_thema_input_dir, "Fuel_Prices.csv")

    def kjor_alt(self):
        self.les_thema_input()
        self.les_bruker_input()
        self.verifiser_input()
        self.utled_input()

        self.set_brensel_df()
        self.set_termisk_df()
        self.set_kapsitet_map()
        self.set_brenselpris_map()

        self.skriv_brenselarkiv_filer()
        self.skriv_lag_pref_filer()
        self.skriv_slett_pref_filer()

    def les_thema_input(self):
        self.hours_df               = get_input_hours_df(self.path_hours)
        self.plant_profiles_df      = get_input_plant_profiles_df(self.path_plant_profiles)
        self.plant_capacities_df    = get_input_plant_capacities_df(self.path_plant_capacities)
        self.plants_df              = get_input_plants_df(self.path_plants)
        self.plant_profile_scen_df  = get_input_plant_profile_scen_df(self.path_plant_profile_scen)
        self.fuels_df               = get_input_fuels_df(self.path_fuels)
        self.fuel_price_profiles_df = get_input_fuel_price_profiles_df(self.path_fuel_price_profiles)
        self.fuel_prices_df         = get_input_fuel_prices_df(self.path_fuel_prices)

    def les_bruker_input(self):
        self.omr_plant_df           = les_omr_plant_df(self.path_xlsx_omr_plant)
        self.fuel_id_brenselnavn_df = les_fuel_id_brenselnavn_df(self.path_xlsx_fuel_id_navn)
        self.ekstra_brensel_df      = les_ekstra_brensel_df(self.path_xlsx_ekstra_brensler)
        self.scenarioer_df          = self.modaar_df


    def verifiser_input(self):
        assert set(self.fuel_id_brenselnavn_df.fuel_id) == set(self.fuels_df.fuel_id), "%s har ikke komplett liste med fuel_id fra thema-modellen" % self.path_xlsx_fuel_id_navn

    def utled_input(self):
        # nyttige dict

        def _map_from_df(df, k, v, ktype, vtype):
            d= dict()
            for __,r in df.iterrows():
                d[ktype(r[k])] = vtype(r[v])
            return d

        # map med alle thema-fuels som brukes som co2
        df = self.fuel_id_brenselnavn_df[self.fuel_id_brenselnavn_df.fuel_id.isin(self.plants_df.carbon_price_id)]
        self.navn_id_co2 = _map_from_df(df, k="brenselnavn", v="fuel_id", ktype=str, vtype=int)

        # map med alle thema-fuels som brukes som fuel
        df = self.fuel_id_brenselnavn_df[self.fuel_id_brenselnavn_df.fuel_id.isin(self.plants_df.fuel_id)]
        self.navn_id_brensel = _map_from_df(df, k="brenselnavn", v="fuel_id", ktype=str, vtype=int)

        # map med alle thema-fuels, uavhengig av om de representerer co2 eller fuel
        self.id_navn_alle_fuels = _map_from_df(df=self.fuel_id_brenselnavn_df, k="fuel_id", v="brenselnavn", ktype=int, vtype=str)

        # map med co2-innhold for alle thema-fuels
        self.id_co2_cont = _map_from_df(df=self.fuels_df, k="fuel_id", v="co2_cont", ktype=int, vtype=float)


    def set_brensel_df(self):
        self.brensel_df = get_brensel_df(self.plants_df, self.omr_plant_df, self.id_navn_alle_fuels, self.id_co2_cont,
                                         self.min_brenselpris_ore_kwh, self.min_co2pris_ore_kwh, self.ekstra_brensel_df,
                                         self.navn_id_brensel, self.navn_id_co2)


    def set_termisk_df(self):
        self.termisk_df = get_termisk_df(self.plants_df, self.id_navn_alle_fuels, 
                                         self.omr_plant_df, self.brensel_df, self.prefnr_start)


    def set_kapsitet_map(self):
        self.kapasitet_map = get_kapasitet_map(self.plant_profile_scen_df, self.plant_profiles_df, self.termisk_df, self.scenarioer_df,
                                               self.plants_df, self.hours_df, self.plant_capacities_df)


    def set_brenselpris_map(self):
        self.brenselpris_map = get_brenselpris_map(self.fuel_prices_df, self.eurnok, self.fuel_price_profiles_df, 
                                                   self.hours_df, self.scenarioer_df)


    def lag_output_mappe(self):
        lag_output_mappe(self.path_output, self.exist_ok)


    def skriv_brenselarkiv_filer(self):
        print(f' - skriver BRENSEL.ARCH')
        skriv_brenselarkiv_filer(self.brensel_df, self.scenarioer_df, self.brenselpris_map, self.antall_aar_data,
                                 self.path_output, self.sluttuke, self.brenselavgift, self.energi_koef, self.filversjon,
                                 self.navn_brenselarkiv_fil, self.kommentar_header, self.kommentar_brensel, self.kommentar_uke)


    def skriv_lag_pref_filer(self):
        print(f' - skriver {self.filnavn_lag_pref_script}')
        kap_dict = self.kapasitet_map[f'{self.modaar}']
        skriv_lag_prefdat_script(self.path_output, self.filnavn_lag_pref_script, self.termisk_df, 'termisk', kap_dict, self.antall_aar_data)


        
    def skriv_slett_pref_filer(self):
        print(f' - skriver {self.filnavn_slett_pref_script}')
        skriv_slett_prefdat_script(self.path_output, self.filnavn_slett_pref_script, self.slett_pref_dict)



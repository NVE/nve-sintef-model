
def get_dos(path_bin, path_hydark):
    miljovar = [("LTM_TEMPERATURKORR", "TEMP3190"),
                ("LTM_DATAPERIODE_25", "HYDRO9797"),
                ("LTM_ENMAGFEEDDB", "v5991MAG"),
                ("LTM_ENMAG_PUMPKORR", "v5991MAG"),
                ("LTM_MPS_AUTKAL", "AUTKAL5035"),
                ("LTM_MPS_FLEKS_OPT", "FLOPT4714"),
                ("LTM_MPS_VVMINP", "SD2002SMT"),
                ("LTM_MPS_KVADRATISKETAP", "KVT524N"),
                ("LTM_MPS_VIND", "VIND2408"),
                ("LTM_MPS_VINDEKSTRA", "VIND2408RA"),
                ("LTM_MPS_EKSOGEN_PRISNIV", "PRIS2011"),
                ("LTM_PRISAVSNITT_MAKS", "MPENM0084"),
                ("LTM_DETMOD_TARC", "FALSE"),
                ("LTM_ARCHIVE", "HYDARK"),
                ("LTM_EXCEL_COMPRESS", "FALSE"),
                ("LTM_MPS_START_STFIL", "FALSE"),
                ("LTM_POWEL_VDL", "Powel_Data"),
                ("LTM_FLEKSI_VANNRESTRIKSJON", "VannforMag"),
                ("LTM_EPF_LASTBEREGN", "LAST3737"),
                ("LTM_EPF_LESKOMBSNITT", "SAML3459"),
                ("LTM_EPF_TAPSBEREGN", "SAMT3685"),
                ("LTM_EPF_SAMNETT", "LINE2013TTRESTR"),
                ("LTM_OPS_SIMTAPEFFEKT", "SIMTAP1234"),
                ("LTM_TERM_LIST", "FALSE"),
                ("ICC_SIM_RESTRICTION_UPPER_OFFSET", "43800"),
                ("ARCHIVE", "HYDARK"), # er denne nodvendig?
                ('LTM_DESIMALTEGN', '"."'),
                ('LTM_KOLONNETEGN', '";"'),
                ("LTM_OPS_ET_PATH", path_bin),
                ("LTM_EMPS_LISENS", "EMPS2142OK"),
                ("HYDARK", path_hydark)]
    lines = []
    for var, val in miljovar:
        lines.append("set %s=%s" % (var, val))
    lines.append("Path %s;%s;" % (path_bin, path_hydark) + "%PATH%")
    string = "\n".join(lines)
    return string

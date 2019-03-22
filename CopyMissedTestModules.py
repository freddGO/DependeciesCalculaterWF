import shutil

CO_SSC_WAVE1_DIR    = "C:\\Users\\aguil001\\eclipse-workspace\\CO\\SMP\\" \
                      "branches\\CO_SSC_WAVE1\\Configuration\\"

CL_TRUNK            = "C:\\Users\\aguil001\\eclipse-workspace\\CL\\SMP" \
                      "\\trunk\\Configuration\\"


DEST_CONFIG_DIR     =   "C:\\Motive\\Telefonica\\Chile\\Config\\100s\\Ganesh-100\\Config_100\\"
                      #"C:\\Motive\\Telefonica\\Chile\\Config\\2\\Config_92\\"

EXT                 = ".xml"
CO                  = "CO"
IVR                 = "IVR"
LOCALE              = "_en_US"


overlay                     = "overlay\\o"
model                       = "model\\"

analysis_ui_definition = "config\\ANALYSIS_UI_DEFINITION_"

testmodule_definition       = "config\\TESTMODULE_DEFINITION_"
testmodule_ui_definition    = "config\\TESTMODULE_UI_DEFINITION_"

testmodule_definition_CO        = "config\\TESTMODULE_DEFINITION_"
testmodule_ui_definition_CO     = "config\\TESTMODULE_UI_DEFINITION_"

overlay_model = [overlay, model]
test_module_definition_list           = [testmodule_definition, testmodule_ui_definition]
test_module_definition_CO_list        = [testmodule_definition_CO, testmodule_ui_definition_CO]


def copy_test_module(missedTMs):
    global EXT, CO, IVR, LOCALE, test_module_definition_CO_list, test_module_definition_list, overlay, model

    for test_module in missedTMs:
        if test_module.startswith(CO) and test_module.endswith(IVR):
            new_test_module_name = test_module[len(CO): len(test_module) - len(IVR)]
            copy_file(overlay + new_test_module_name + EXT, "overlay\\")
            copy_file(model + new_test_module_name + EXT, "model\\")
            for t in test_module_definition_CO_list:
                copy_file(t + test_module + LOCALE, "config\\")

        else:

            copy_file(overlay + test_module + EXT, "overlay\\")
            copy_file(model + test_module + EXT, "model\\")
            copy_file(analysis_ui_definition + test_module + LOCALE, "config\\")
            for t in test_module_definition_list:
                copy_file(t + test_module + LOCALE, "config\\")


        print ("\n")

def copy_file(file, des_folder):
    global CO_SSC_WAVE1_DIR
    global DEST_CONFIG_DIR
    try:
        origin_file = CL_TRUNK + file
        destination_file_dir = DEST_CONFIG_DIR + des_folder
        shutil.copy(origin_file, destination_file_dir)
        print("[INFO] "  + file + " - has been copied to " + destination_file_dir)
    except shutil.Error as e:
        print("[ERROR] %s" % e )
    except IOError as e:
        print("[ERROR] IO  %s " %e.strerror)
        print(origin_file)
        print(destination_file_dir)

####list_of_missed_tm = ["COCustomerTechnicalIncidentsIVR","SubscriberInitializationOnDemand","COCustomerRequestsIVR"]

list_of_missed_tm = ["CTCreateTicket"]
copy_test_module(list_of_missed_tm)

#name = "COCustomerTechnicalIncidentsIVR"
#print (name.startswith(CO))
#print (name.endswith(IVR))

#new_test_modulename = name[len(CO): len(name) - len(IVR)]
#print (name)
###print (new_test_module_name)
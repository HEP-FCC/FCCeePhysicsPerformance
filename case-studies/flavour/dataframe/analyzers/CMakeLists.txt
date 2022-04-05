
find_package(ROOT REQUIRED COMPONENTS ROOTDataFrame ROOTVecOps)
include(${ROOT_USE_FILE})

find_package(EDM4HEP)
find_package(podio)
find_package(Vdt)


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

get_target_property(EDM4HEP_INCLUDE_DIRS EDM4HEP::edm4hep INTERFACE_INCLUDE_DIRECTORIES)

include_directories(${EDM4HEP_INCLUDE_DIRS} ${podio_INCLUDE_DIR})

ROOT_GENERATE_DICTIONARY(G__FCCAnalysesFlavour Bs2JPsiPhi.h Bs2DsK.h dummyLoaderFlavour.h LINKDEF LinkDef.h)


file(GLOB sources *.cc)
file(GLOB headers *.h)
add_library(FCCAnalysesFlavour SHARED ${sources} ${headers} G__FCCAnalysesFlavour.cxx )
target_include_directories(FCCAnalysesFlavour  PUBLIC
                           ${CMAKE_SOURCE_DIR}/analyzers
	                         ${FCCANALYSES_INCLUDE_PATH}
                           ${VDT_INCLUDE_DIR}
                          )
target_link_libraries(FCCAnalysesFlavour
                      ROOT::Physics 
                      ROOT::MathCore
                      ROOT::ROOTVecOps
                      ROOT::ROOTDataFrame
                      EDM4HEP::edm4hep
                      EDM4HEP::edm4hepDict
                      podio::podio
                      )

set_target_properties(FCCAnalysesFlavour
                      PROPERTIES PUBLIC_HEADER "${headers}")

install(TARGETS FCCAnalysesFlavour
        RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
        LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
        PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/FCCAnalysesFlavour"
        COMPONENT dev
        )

install(FILES
        "${PROJECT_BINARY_DIR}/analyzers/libFCCAnalysesFlavour.rootmap"
        DESTINATION "${INSTALL_LIB_DIR}"
        COMPONENT dev
        )

if (${ROOT_VERSION} GREATER 6)
    install(FILES
            "${PROJECT_BINARY_DIR}/analyzers/libFCCAnalysesFlavour_rdict.pcm"
            DESTINATION "${INSTALL_LIB_DIR}"
            COMPONENT dev)
endif()

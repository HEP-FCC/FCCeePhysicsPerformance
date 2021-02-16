
find_package(ROOT REQUIRED COMPONENTS ROOTDataFrame ROOTVecOps)
include(${ROOT_USE_FILE})
#include("${ROOT_DIR}/modules/RootNewMacros.cmake")

find_package(EDM4HEP)
find_package(podio)


set(CMAKE_MODULE_PATH ${CMAKE_CURRENT_SOURCE_DIR}/cmake ${CMAKE_MODULE_PATH})

get_target_property(EDM4HEP_INCLUDE_DIRS EDM4HEP::edm4hep INTERFACE_INCLUDE_DIRECTORIES)

include_directories(${EDM4HEP_INCLUDE_DIRS} ${podio_INCLUDE_DIR})

ROOT_GENERATE_DICTIONARY(G__Bs2JPsiPhi Bs2JPsiPhi.h Bs2DsK.h dummyLoader.h LINKDEF Bs2JPsiPhiLinkDef.h)


file(GLOB sources *.cc)
file(GLOB headers *.h)
add_library(Bs2JPsiPhi SHARED ${sources} ${headers} G__Bs2JPsiPhi.cxx )
target_include_directories(Bs2JPsiPhi  PUBLIC
        ${CMAKE_SOURCE_DIR}/analyzers/dataframe
	$ENV{LOCALFCCANALYSES}
)
target_link_libraries(Bs2JPsiPhi ROOT::Physics ROOT::MathCore ROOT::ROOTVecOps ROOT::ROOTDataFrame EDM4HEP::edm4hep EDM4HEP::edm4hepDict podio::podio)

set_target_properties(Bs2JPsiPhi PROPERTIES
  PUBLIC_HEADER "${headers}")

install(TARGETS Bs2JPsiPhi
    RUNTIME DESTINATION "${INSTALL_BIN_DIR}" COMPONENT bin
    LIBRARY DESTINATION "${INSTALL_LIB_DIR}" COMPONENT shlib
    PUBLIC_HEADER DESTINATION "${INSTALL_INCLUDE_DIR}/Bs2JPsiPhi"
    COMPONENT dev
    )

install(FILES
  "${PROJECT_BINARY_DIR}/analyzers/dataframe/libBs2JPsiPhi.rootmap"
    DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)

if (${ROOT_VERSION} GREATER 6)
    install(FILES
          "${PROJECT_BINARY_DIR}/analyzers/dataframe/libBs2JPsiPhi_rdict.pcm"
                DESTINATION "${INSTALL_LIB_DIR}" COMPONENT dev)
    endif()

StoreGateKeys = [
        'EventInfo/ByteStreamEventInfo', # <---
        'MdtCsmContainer/MDTCSM', 
        'RpcPadContainer/RPCPAD'
    ]

def setup_bs_input(files):
    global StoreGateKeys
    #
    theApp.Dlls += ['ByteStreamCnvSvcBase']
    theApp.ExtSvc += ['ROBDataProviderSvc']
    theApp.Dlls += ['ByteStreamCnvSvc']
    theApp.ExtSvc += ['ByteStreamEventStorageV2InputSvc/ByteStreamInputSvc']
    theApp.ExtSvc += ['EventSelectorByteStream/EventSelector']
    theApp.EvtSel = 'EventSelector'
    EventSelector = Service('EventSelector')
    EventSelector.ByteStreamInputSvc = 'ByteStreamInputSvc'
    ByteStreamInputSvc = Service('ByteStreamInputSvc')
    ByteStreamInputSvc.FullFileName = files  # <===

    # Proxy provider for StoreGate.
    EventPersistency = Service('EventPersistencySvc')
    EventPersistency.CnvServices += ['ByteStreamCnvSvc']
    EventPersistency.CnvServices += ['ByteStreamEventStorageInputSvc']
    ProxyProviderSvc = Service('ProxyProviderSvc')
    ProxyProviderSvc.ProviderNames += [
        'ByteStreamAddressProviderSvc'
        ]
    ByteStreamAddressProviderSvc = Service('ByteStreamAddressProviderSvc')
    include('ByteStreamCnvSvcBase/BSAddProvSvc_RDO_jobOptions.py')
    ByteStreamAddressProviderSvc.TypeNames += StoreGateKeys

def setup_pool_input(files):
    theApp.Dlls += ['ByteStreamCnvSvcBase']
    theApp.ExtSvc += ['ROBDataProviderSvc']
    include('AthenaPoolCnvSvc/AthenaPool_jobOptions.py')
    theApp.Dlls += ['EventSelectorAthenaPool']
    theApp.ExtSvc += ['EventSelectorAthenaPool/EventSelector']
    theApp.EvtSel = 'EventSelector'
    ProxyProviderSvc = Service('ProxyProviderSvc')
    ProxyProviderSvc.ProviderNames += ['EventSelector']
    EventSelector = Service('EventSelector')
    EventSelector.InputCollections = files
    # POOL converters
    include('EventAthenaPool/EventAthenaPool_joboptions.py')
    include('MuonEventAthenaPool/MuonEventAthenaPool_joboptions.py')

def setup_geometry():
    print 'Setups for geometry'
    DetDescrVersion = 'ATLAS-DC3-02'
    include('EventInfo/EventInfo_joboptions.py')
    include('EventInfoMgt/EventInfoMgt_jobOptions.py')
    include('RDBAccessSvc/RDBAccessSvcPdb_jobOptions.py')
    include('AtlasGeoModel/SetGeometryVersion.py')
    include('AtlasGeoModel/MuonGeoModel.py')
    theApp.Dlls += ['GeoModelSvc']
    theApp.ExtSvc += ['GeoModelSvc/GeoModelSvc']
    GeoModelSvc = Service('GeoModelSvc')
    DetDescrCnvSvc = Service('DetDescrCnvSvc')
    DetDescrCnvSvc.IdDictGlobalTag = 'initial_layout'
    DetDescrCnvSvc.MuonIDFileName = 'IdDictParser/IdDictMuonSpectrometer_Q.02.xml'

def setup_database():
    print 'Setups for database'

#---------------------------------------------------------------------------
# tdaq_tools.py
#---------------------------------------------------------------------------

def convertMuonRoIWord(word_in_muctpi_rod_data):
  """Convert the muon RoI word stored in the MUCTPI ROD data into the
  format used in the RoI word sent to LVL2"""
  daqData = word_in_muctpi_rod_data
  first = (daqData >> 25) & 0x1
  secAddress = (daqData >> 17) & 0xff
  lvl2Word = 0
  lvl2Word |= (first << 22);
  lvl2Word |= (secAddress << 14);
  lvl2Word |= (daqData & 0x1fff);
  # add one to RoI number
  lvl2Word |= (1<<2)
  return lvl2Word


def cp_header(out, src):
  out.source_id(src.source_id())
  out.run_no(src.run_no())
  out.lvl1_id(src.lvl1_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  out.bc_id(src.bc_id())
  # out.status(src.status())
  print 'gno9'
  print 'obj lvl1_id: ', out.lvl1_id()
  print 'obj source_id: ', out.source_id()
  print 'obj bc_id: ', out.bc_id()

def cp_event_header(out, src):
  out.source_id(src.source_id())
  out.run_no(src.run_no())
  out.lvl1_id(src.lvl1_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  #cp_header(out, src)
  #out.run_type(src.run_type())
  #out.lvl1_trigger_type(src.lvl1_trigger_type())
  #out.lvl2_trigger_info(src.lvl2_trigger_info())
  #out.event_filter_info(src.event_filter_info())
  out.stream_tag(src.stream_tag())
  out.bc_time(src.bc_time())
  out.detector_mask(src.detector_mask())
  out.global_id(src.global_id())
  out.lumi_block(src.lumi_block())
  print 'obj run_no: ', out.run_no()

def cp_subdet_header(out, src):
  out.source_id(src.source_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  #return cp_header(out, src)

def cp_ros_header(out, src):
  return cp_header(out, src)

def cp_rob_header(out, src):
  out.source_id(src.source_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  # cp_header(out, src)
  #out.rod_header(src.rod_header())
  out.rod_status(src.rod_status())
  out.rod_trailer(src.rod_trailer())
  out.rod_bc_id(src.rod_bc_id())
  out.rod_detev_type(src.rod_detev_type())
  out.rod_lvl1_id(src.rod_lvl1_id())
  out.rod_lvl1_type(src.rod_lvl1_type())
  out.rod_run_no(src.rod_run_no())
  out.status_position(src.status_position())

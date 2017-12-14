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
  lvl2Word |= (daqData & 0x1ffff);
  # add one to RoI number
  lvl2Word |= (1<<2)+(1<<11)
  return lvl2Word

def toSimpleList(array):
  x = []
  for b in array:
    x.append(b)
  return x

def cp_header(out, src):
  out.source_id(src.source_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  out.run_no(src.run_no())
  out.lvl1_id(src.lvl1_id())
  out.bc_id(src.bc_id())
  out.status(toSimpleList(src.status()))
  # out.status(src.status())

def cp_event_header(out, src):
  out.source_id(src.source_id())
  out.run_no(src.run_no())
  out.lvl1_id(src.lvl1_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  #cp_header(out, src)
  # out.run_type(src.run_type())
  #out.lvl1_trigger_type(src.lvl1_trigger_type())
  #out.lvl2_trigger_info(src.lvl2_trigger_info())
  #out.event_filter_info(src.event_filter_info())
  #out.stream_tag(src.stream_tag())
  #out.bc_time(src.bc_time())
  #out.detector_mask(src.detector_mask())
  out.global_id(src.global_id())
  #out.lumi_block(src.lumi_block())

def cp_subdet_header(out, src):
  out.source_id(src.source_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  #return cp_header(out, src)

def cp_ros_header(out, src):
  return cp_header(out, src)

def cp_rob_header(out, src):
  out.source_id(src.source_id())
  out.minor_version( (src.version().major()<<16) + src.version().minor())
  out.rod_detev_type(src.rod_detev_type())
  out.rod_run_no(src.rod_run_no())
  out.rod_lvl1_id(src.rod_lvl1_id())
  out.rod_bc_id(src.rod_bc_id())
  out.status(toSimpleList(src.status()))
  out.rod_status(toSimpleList(src.status()))
  # cp_header(out, src)
  #out.rod_header(src.rod_header())
  #out.rod_status(src.rod_status())
  #out.rod_trailer(src.rod_trailer())
  #out.rod_lvl1_type(src.rod_lvl1_type())
  #out.status_position(src.status_position())

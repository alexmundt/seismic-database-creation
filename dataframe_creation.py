import obspy
import numpy as np
import pandas as pd

# this function 
def create_dataframe_from_catalog(catalog):
    """ A function that creates a pandas dataframe from a catalog using the information contained in the obspy catalog object including the normalized moment tensor 
    """
    cat = catalog
    
    lons = []
    lats = []
    depths = []
    times = []
    mags = []
    mag_types = []
    m_rrs = []
    m_tts = []
    m_pps = []
    m_rts = []
    m_rps = []
    m_tps = []
    source_time_durations = []
    source_time_functions = []
    
    gcmt_ids = []

    m_rr_norms = []
    m_tt_norms = []
    m_pp_norms = []
    m_rt_norms = []
    m_rp_norms = []
    m_tp_norms = []

    for e in cat:

        lon = e.preferred_origin().longitude
        lat = e.preferred_origin().latitude
        depth = e.preferred_origin().depth
        time =e.preferred_origin().time

        mag = e.preferred_magnitude().mag
        mag_type = e.preferred_magnitude().magnitude_type

        m_rr = e.preferred_focal_mechanism().moment_tensor.tensor.m_rr
        m_tt = e.preferred_focal_mechanism().moment_tensor.tensor.m_tt
        m_pp = e.preferred_focal_mechanism().moment_tensor.tensor.m_pp
        m_rt = e.preferred_focal_mechanism().moment_tensor.tensor.m_rt
        m_rp = e.preferred_focal_mechanism().moment_tensor.tensor.m_rp
        m_tp = e.preferred_focal_mechanism().moment_tensor.tensor.m_tp

        source_time_duration = e.preferred_focal_mechanism().moment_tensor.source_time_function.duration
        source_time_function = e.preferred_focal_mechanism().moment_tensor.source_time_function.type

        id_string = e.resource_id.id
        id_string = id_string.replace("smi:local/ndk/", "")
        id_string = id_string.replace("/event","")
        gcmt_id = id_string

        lons.append(lon)
        lats.append(lat)
        depths.append(depth)
        times.append(time)
        mags.append(mag)
        mag_types.append(mag_type)
        m_rrs.append(m_rr)
        m_tts.append(m_tt)
        m_pps.append(m_pp)
        m_rts.append(m_rt)
        m_rps.append(m_rp)
        m_tps.append(m_tp)

        source_time_durations.append(source_time_duration)
        source_time_functions.append(source_time_function)

        gcmt_ids.append(gcmt_id)
        
        # normalize the values of the moment tensor
        max_value = max(np.abs(m_rr),np.abs(m_tt), np.abs(m_pp), np.abs(m_rt), np.abs(m_rp), np.abs(m_tp))
        m_rr_norm = m_rr/max_value
        m_tt_norm = m_tt/max_value
        m_pp_norm = m_pp/max_value
        m_rt_norm = m_rt/max_value
        m_rp_norm = m_rp/max_value
        m_tp_norm = m_tp/max_value

        m_rr_norms.append(m_rr_norm)
        m_tt_norms.append(m_tt_norm)
        m_pp_norms.append(m_pp_norm)
        m_rt_norms.append(m_rt_norm)
        m_rp_norms.append(m_rp_norm)
        m_tp_norms.append(m_tp_norm)
        
    # now create a dictionary with all the values
    data_dict = {"longitude":lons, "latitude":lats, "depth": depths, "time":times, "mag":mags, "mag_type":mag_types, "m_rr":m_rrs,
            "m_tt":m_tts, "m_pp":m_pps, "m_rt":m_rts, "m_rp":m_rps, "m_tp":m_tps, "source_time_duration":source_time_durations,
            "source_time_function":source_time_functions,
            "gcmt_id":gcmt_ids,
            "m_rr_norm":m_rr_norms,
            "m_tt_norm":m_tt_norms,
            "m_pp_norm":m_pp_norms,
            "m_rt_norm":m_rt_norms,
            "m_rp_norm":m_rp_norms,
            "m_tp_norm":m_tp_norms}
    
    # finally: create a dataframe from the dictionary
    frame = pd.DataFrame.from_dict(data_dict)

    return frame
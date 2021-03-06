"""Xiaomi aqara single key wall switch devices."""
import logging

from zigpy.profiles import zha
from zigpy.zcl.clusters.general import (
    AnalogInput,
    Basic,
    BinaryOutput,
    DeviceTemperature,
    Groups,
    Identify,
    MultistateInput,
    OnOff,
    Ota,
    Scenes,
    Time,
)

from zhaquirks import Bus
from zhaquirks.xiaomi import (
    LUMI,
    AnalogInputCluster,
    BasicCluster,
    OnOffCluster,
    XiaomiCustomDevice,
    XiaomiPowerConfiguration,
)

from . import BasicClusterDecoupled, WallSwitchMultistateInputCluster
from .. import (
    LUMI,
    AnalogInputCluster,
    OnOffCluster,
    XiaomiCustomDevice,
    XiaomiPowerConfiguration,
)
from ...const import (
    ARGS,
    ATTRIBUTE_ID,
    ATTRIBUTE_NAME,
    BUTTON,
    BUTTON_2,
    CLUSTER_ID,
    COMMAND,
    COMMAND_ATTRIBUTE_UPDATED,
    COMMAND_CLICK,
    COMMAND_DOUBLE,
    DEVICE_TYPE,
    ENDPOINT_ID,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
    SKIP_CONFIGURATION,
    VALUE,
)

ATTRIBUTE_PRESENT_VALUE = "present_value"

_LOGGER = logging.getLogger(__name__)


class CtrlLn(XiaomiCustomDevice):
    """Aqara double key switch device."""

    def __init__(self, *args, **kwargs):
        """Init."""
        self.power_bus = Bus()
        super().__init__(*args, **kwargs)

    signature = {
        MODELS_INFO: [(LUMI, "lumi.ctrl_ln1.aq1"), (LUMI, "lumi.ctrl_ln2.aq1")],
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    Basic.cluster_id,
                    XiaomiPowerConfiguration.cluster_id,
                    DeviceTemperature.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOff.cluster_id,
                    Time.cluster_id,
                    BinaryOutput.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [OnOff.cluster_id, BinaryOutput.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.MAIN_POWER_OUTLET,
                INPUT_CLUSTERS: [AnalogInput.cluster_id],
                OUTPUT_CLUSTERS: [Groups.cluster_id, AnalogInput.cluster_id],
            },
            4: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.METER_INTERFACE,
                INPUT_CLUSTERS: [AnalogInput.cluster_id],
                OUTPUT_CLUSTERS: [AnalogInput.cluster_id],
            },
            5: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [MultistateInput.cluster_id, BinaryOutput.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
            6: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [MultistateInput.cluster_id, BinaryOutput.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
            7: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [MultistateInput.cluster_id, BinaryOutput.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
        },
    }

    replacement = {
        SKIP_CONFIGURATION: True,
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [
                    BasicClusterDecoupled,
                    XiaomiPowerConfiguration,
                    DeviceTemperature.cluster_id,
                    Identify.cluster_id,
                    Groups.cluster_id,
                    Scenes.cluster_id,
                    OnOffCluster,
                    Time.cluster_id,
                    BinaryOutput.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Time.cluster_id, Ota.cluster_id],
            },
            2: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.SMART_PLUG,
                INPUT_CLUSTERS: [OnOffCluster, BinaryOutput.cluster_id],
                OUTPUT_CLUSTERS: [],
            },
            3: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.MAIN_POWER_OUTLET,
                INPUT_CLUSTERS: [AnalogInputCluster],
                OUTPUT_CLUSTERS: [Groups.cluster_id, AnalogInput.cluster_id],
            },
            5: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    WallSwitchMultistateInputCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
            6: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    WallSwitchMultistateInputCluster,
                ],
                OUTPUT_CLUSTERS: [],
            },
        },
    }

    device_automation_triggers = {
        (COMMAND_CLICK, BUTTON): {
            ENDPOINT_ID: 5,
            CLUSTER_ID: 18,
            COMMAND: COMMAND_ATTRIBUTE_UPDATED,
            ARGS: {ATTRIBUTE_ID: 85, ATTRIBUTE_NAME: ATTRIBUTE_PRESENT_VALUE, VALUE: 1},
        },
        (COMMAND_DOUBLE + COMMAND_CLICK, BUTTON): {
            ENDPOINT_ID: 5,
            CLUSTER_ID: 18,
            COMMAND: COMMAND_ATTRIBUTE_UPDATED,
            ARGS: {ATTRIBUTE_ID: 85, ATTRIBUTE_NAME: ATTRIBUTE_PRESENT_VALUE, VALUE: 2},
        },
        (COMMAND_CLICK, BUTTON_2): {
            ENDPOINT_ID: 6,
            CLUSTER_ID: 18,
            COMMAND: COMMAND_ATTRIBUTE_UPDATED,
            ARGS: {ATTRIBUTE_ID: 85, ATTRIBUTE_NAME: ATTRIBUTE_PRESENT_VALUE, VALUE: 1},
        },
        (COMMAND_DOUBLE + COMMAND_CLICK, BUTTON_2): {
            ENDPOINT_ID: 6,
            CLUSTER_ID: 18,
            COMMAND: COMMAND_ATTRIBUTE_UPDATED,
            ARGS: {ATTRIBUTE_ID: 85, ATTRIBUTE_NAME: ATTRIBUTE_PRESENT_VALUE, VALUE: 2},
        },
    }

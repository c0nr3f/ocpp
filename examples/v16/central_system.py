import asyncio
from re import L
import websockets
from datetime import datetime
import logging
logging.getLogger('ocpp').setLevel(level=logging.DEBUG)
logging.getLogger('ocpp').addHandler(logging.StreamHandler())

from ocpp.routing import on
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *
from ocpp.v16 import call_result, call

class ChargePoint(cp):

    # Operations Initiated by Central System

    async def send_cancel_reservation(self):
        request = call.CancelReservationPayload(
            reservation_id=1
        )

        response = await self.call(request)

        if response.status == CancelReservationStatus.accepted:
            print("Reservation for the identifier has been cancelled.")

        elif response.status == CancelReservationStatus.accepted:
            print("Reservation could not be cancelled, because there is no reservation active for the identifier.")

    async def send_change_availability(self):
        request = call.ChangeAvailabilityPayload(
            connector_id=1,
            type=AvailabilityType.operative
        )

        response = await self.call(request)

        if response.status == AvailabilityStatus.accepted:
            print("Request has been accepted and will be executed.")

        elif response.status == AvailabilityStatus.rejected:
            print("Request has not been accepted and will not be executed.")
        
        elif response.status == AvailabilityStatus.scheduled:
            print("Request has been accepted and will be executed when transaction(s) in progress have finished.")

    async def send_change_configuration(self, key, value):
        request = call.ChangeConfigurationPayload(
            # key and value of the conf setting to change
            key=key,
            value=value
        )

        response = await self.call(request)

        if response.status == ConfigurationStatus.accepted:
            print("Configuration key supported and setting has been changed.")

        elif response.status == ConfigurationStatus.rejected:
            print("Configuration key supported, but setting could not be changed.")
        
        elif response.status == ConfigurationStatus.reboot_required:
            print("Configuration key supported and setting has been changed, but change will be available after reboot (Charge Point will not reboot itself)")
        
        elif response.status == ConfigurationStatus.not_supported:
            print("Request has been accepted and will be executed when transaction(s) in progress have finished.")

    async def send_clear_cache(self):
        request = call.ClearCachePayload()

        response = await self.call(request)

        if response.status == ClearCacheStatus.accepted:
            print("Command has been executed.")

        elif response.status == ClearCacheStatus.rejected:
            print("Command has not been executed.")
        
    async def send_clear_charging_profile(self):
        request = call.ClearChargingProfilePayload(
            id=1,
            connector_id=1,
            charging_profile_purpose="ChargePointMaxProfile" # or TxDefaultProile or TxProfile
        )

        response = await self.call(request)

        if response.status == ChargingProfileStatus.accepted:
            print("Request has been accepted and will be executed.")

        elif response.status == ChargingProfileStatus.rejected:
            print("Request has not been accepted and will not be executed.")

        elif response.status == ChargingProfileStatus.not_supported:
            print("Charge Point indicates that the request is not supported.")

    async def send_data_transfer(self):
        request = call.DataTransferPayload(
            vendor_id=1,
            message_id=1,
            data=0
            )

        response = await self.call(request)

        if response.status == DataTransferStatus.accepted:
            print("Message has been accepted and the contained request is accepted.")

        elif response.status == DataTransferStatus.rejected:
            print("Message has been accepted but the contained request is rejected.")

        elif response.status == DataTransferStatus.unknown_message_id:
            print("Message could not be interpreted due to unknown messageId string.")

        elif response.status == DataTransferStatus.unknown_vendor_id:
            print("Message could not be interpreted due to unknown vendorId string.")

        data = response.data

    async def send_get_composite_schedule(self):
        request = call.GetCompositeSchedulePayload(
            connector_id=1,
            duration=10,
            charging_rate_unit="W" # W für Leistung oder A für Strom
        )

        response = await self.call(request)

        if response.status == GetCompositeScheduleStatus.accepted:
            print("Request has been accepted and will be executed.")

        elif response.status == ChargingProfileStatus.rejected:
            print("Request has not been accepted and will not be executed.")

    async def send_get_configuration(self):
        request = call.GetConfigurationPayload(
            # key=1 # Optional. List of keys for which the configuration value is requested.
        )

        response = await self.call(request)

        configurationKey = response.configurationKey
        unknownKey = response.unknownKey

    async def send_get_diagnostics(self):
        request = call.GetDiagnosticsPayload(
            location='/path/to/directory',
            retries=5
        )

        response = await self.call(request)

        fileName = response.fileName

    async def send_get_local_list_version(self):
        request = call.GetLocalListVersionPayload()

        response = await self.call(request)

        listVersion = response.listVersion

    async def send_remote_start_transaction(self):
        request = call.RemoteStartTransactionPayload(
            id_tag=1,
            connector_id=1,
            charging_profile=1
        )

        response = await self.call(request)

        if response.status == RemoteStartStopStatus.accepted:
            print("Command will be executed.")

        elif response.status == ChargingProfileStatus.rejected:
            print("Command will not be executed.")

    async def send_remote_stop_transaction(self):
        request = call.RemoteStopTransactionPayload(
            transaction_id=1
        )

        response = await self.call(request)

        if response.status == RemoteStartStopStatus.accepted:
            print("Command will be executed.")

        elif response.status == RemoteStartStopStatus.rejected:
            print("Command will not be executed.")

    async def send_reserve_now(self):
        request = call.ReserveNowPayload(
            connector_id=1,
            expiry_date=datetime.utcnow().isoformat(),
            id_tag=1
        )

        response = await self.call(request)

        if response.status == ReservationStatus.accepted:
            print("Reservation has been made.")

        elif response.status == ReservationStatus.faulted:
            print("Reservation has not been made, because connectors or specified connector are in a faulted state.")

        elif response.status == ReservationStatus.occupied:
            print("Reservation has not been made. All connectors or the specified connector are occupied.")

        elif response.status == ReservationStatus.rejected:
            print("Reservation has not been made. Charge Point is not configured to accept reservations.")

        elif response.status == ReservationStatus.unavailable:
            print("Reservation has not been made, because connectors or specified connector are in an unavailable state.")

    async def send_reset(self):
        request = call.ResetPayload(
            type='hard' # or soft
        )

        response = await self.call(request)

        if response.status == ResetStatus.accepted:
            print("Command will be executed.")

        elif response.status == ResetStatus.rejected:
            print("Command will not be executed.")

    async def send_local_list(self):
        request = call.SendLocalListPayload(
            list_version=1,
            update_type='full' # or differential
        )

        response = await self.call(request)

        if response.status == UpdateStatus.accepted:
            print("Local Authorization List successfully updated.")

        elif response.status == UpdateStatus.failed:
            print("Failed to update the Local Authorization List.")

        elif response.status == UpdateStatus.not_supported:
            print("Update of Local Authorization List is not supported by Charge Point.")

        elif response.status == UpdateStatus.version_mismatch:
            print("Version number in the request for a differential update is less or equal then version number of current list.")

    async def send_set_charging_profiles(self):
        request = call.SetChargingProfilePayload(
            connector_id=1,
            cs_charging_profiles={
                'chargingProfileId':1,
                'stackLevel':1,
                'chargingProfilePurpose':'ChargePointMaxProfile',
                'chargingProfileKind':'Absolute', # or Recurring or Relative
                'chargingSchedulePeriod':{
                    'chargingRateUnit':'W', # Power or Ampere
                    'chargingSchedulePeriod':{
                        'startPeriod':1,
                        'limit':10 # Power limit in Ampere
                    }
                }
            }
        )

        response = await self.call(request)

        if response.status == ChargingProfileStatus.accepted:
            print("Request has been accepted and will be executed.")

        elif response.status == ChargingProfileStatus.rejected:
            print("Request has not been accepted and will not be executed.")

        elif response.status == ChargingProfileStatus.not_supported:
            print("Charge Point indicates that the request is not supported.")

    async def send_trigger_message(self):
        # triggert message nach Wahl
        request = call.TriggerMessagePayload(
            requested_message='BootNotification' 
            # or: DiagnosticsStatusNotification,
            #     FirmwareStatusNotification,
            #     Heartbeat,
            #     MeterValues,
            #     StatusNotification
        )

        response = await self.call(request)

        if response.status == TriggerMessageStatus.accepted:
            print("Requested notification will be sent.")

        elif response.status == TriggerMessageStatus.rejected:
            print("Requested notification will not be sent.")

        elif response.status == TriggerMessageStatus.not_implemented:
            print("Requested notification cannot be sent because it is either not implemented or unknown.")

    async def send_unlock_connector(self):
        # triggert message nach Wahl
        request = call.UnlockConnectorPayload(
            connector_id=1
        )

        response = await self.call(request)

        if response.status == UnlockStatus.unlocked:
            print("Connector has successfully been unlocked.")

        elif response.status == UnlockStatus.unlock_failed:
            print("Failed to unlock the connector.")

        elif response.status == UnlockStatus.not_supported:
            print("Charge Point has no connector lock.")

    async def send_update_firmware(self):
        # triggert message nach Wahl
        request = call.UpdateFirmwarePayload(
            location='/path/to/file',
            retrieve_date=datetime.utcnow().isoformat()
        )

        response = await self.call(request)

    # Operations Initiated by Charge Point

    @on(Action.Authorize)
    def on_authorize(self, id_tag, **kwargs):
        if id_tag == 'AA123D3F' or id_tag == 'FED4269':
            status = 'Accepted'
        
        else:
            status = 'Invalid'

        return call_result.AuthorizePayload(
            id_tag_info={'status': status}
        )

    @on(Action.BootNotification)
    def on_boot_notitication(self, charge_point_vendor, charge_point_model, **kwargs):

        print(f'{charge_point_model} from {charge_point_vendor} booted.')

        return call_result.BootNotificationPayload(
            current_time=datetime.utcnow().isoformat(),
            interval=10,
            status=RegistrationStatus.accepted
        )
    
    @on(Action.DataTransfer)
    def on_datatransfer(self, vendor_id, **kwargs):
        return call_result.DataTransferPayload(
            status=DataTransferStatus.accepted
        )

    @on(Action.DiagnosticsStatusNotification)
    def on_diagnosticsstatusnotification(self, status, **kwargs):
        return call_result.DiagnosticsStatusNotificationPayload()

    @on(Action.FirmwareStatusNotification)
    def on_firmwarestatusnotification(self, status, **kwargs):
        return call_result.FirmwareStatusNotificationPayload()

    @on(Action.Heartbeat)
    def on_heartbeat(self, **kwargs):
        return call_result.HeartbeatPayload(
            current_time=datetime.utcnow().isoformat()
        )

    @on(Action.MeterValues)
    def on_metervalues(self, connector_id, meter_value, **kwargs):
        return call_result.MeterValuesPayload()
  
    @on(Action.StartTransaction)
    def on_starttransaction(self, connector_id, id_tag, meter_start, timestamp, **kwargs):
        return call_result.StartTransactionPayload(
            transaction_id=1,
            id_tag_info={'status': 'Accepted'}
        )

    @on(Action.StatusNotification)
    def on_status_notitication(self, connector_id, error_code, status, **kwargs):
        return call_result.StatusNotificationPayload()

    @on(Action.StopTransaction)
    def on_stoptransaction(self, id_tag, meter_stop, timestamp, transaction_id, reason, **kwargs):
        return call_result.StopTransactionPayload()

# Server functions

async def on_connect(websocket, path):
    """ For every new charge point that connects, create a ChargePoint instance
    and start listening for messages.

    """
    #await websocket.send('Connection made succesfully.')
    charge_point_id = path.strip('/')
    print(f'Charge point {charge_point_id} connected')

    cp = ChargePoint(charge_point_id, websocket)
    await cp.start()


async def main():
    server = await websockets.serve(
        on_connect,
        '0.0.0.0',
        9000,
        subprotocols=['ocpp1.6']
    )

    await server.wait_closed()


if __name__ == '__main__':
    asyncio.run(main())

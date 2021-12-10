import asyncio
import logging
from datetime import datetime
from os import error
from typing import AnyStr
import websockets

from ocpp.v16 import call
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import AvailabilityType, RegistrationStatus, ChargePointErrorCode, ChargePointStatus

logging.basicConfig(level=logging.INFO)


class ChargePoint(cp):
    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Python ",
            charge_point_vendor="Test Script",
            charge_box_serial_number="1337",
            charge_point_serial_number="420",
            firmware_version="69",
            iccid="FED42",
            imsi="1234ABCD",
            meter_serial_number="1A2B3C4D",
            meter_type="nice_meter"
        )

        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            logging.info("Connected to central system.")
        elif response.status == RegistrationStatus.rejected:
            logging.info("Central system rejected the connection!")

    async def change_availablity(self):
        request = call.ChangeAvailabilityPayload(
            connector_id= 1,
            type=AvailabilityType.operative # .inoperative
        )

        response = await self.call(request)

        if response.status == AvailabilityType.operative:
            logging.info("System available.")
        elif response.status == AvailabilityType.operative:
            logging.info("System not available.")

    async def send_heartbeat(self):
        while True:
            try:
                request = call.HeartbeatPayload()                              
                response = await self.call(request)
                # Heartbeat rate in sec
                await asyncio.sleep(10)
            except:
                raise


    async def send_authorize(self):
        request = call.AuthorizePayload(
            id_tag='FED4269'
        )

        response = await self.call(request)

        if response.id_tag_info["status"] == "Accepted":
            logging.info("Authorization successful")
            return True
        else:
            logging.info("Authorization unsuccessful")
            return False

    async def start_transaction(self):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag='FED426',
            meter_start=0,          # Initial Energy meter value / integer
            timestamp=datetime.utcnow().isoformat()
            # reservation_id=1
        )

        response = await self.call(request)

        if response.id_tag_info["status"] == "Accepted":
            logging.info("Start Charging ...")
            return response.transaction_id
        else:
            logging.info("Problems with starting the charge process!")

    async def stop_transaction(self, transaction_id):
        request = call.StopTransactionPayload(
            transaction_id=transaction_id,
            meter_stop=1,          # Initial Energy meter value / integer
            timestamp=datetime.utcnow().isoformat()
        )

        response = await self.call(request)

        if response.id_tag_info["status"] == "Accepted":
            print("Charging stopped.")
        else:
            print("Error in executing StopTransaction!")
    
    async def send_status_notification(self, code):
        if code == "no_error":
            error_code=ChargePointErrorCode.no_error
        else:
            error_code=ChargePointErrorCode.other_error

        request = call.StatusNotificationPayload(
            connector_id=1,
            error_code=error_code,
            status=ChargePointStatus.available
        )

        response = await self.call(request)

async def main():
    async with websockets.connect(
        'ws://localhost:9000/CP_3',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_3', ws)

        await asyncio.gather(cp.start(), cp.send_heartbeat())

if __name__ == '__main__':
    asyncio.run(main())

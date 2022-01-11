import asyncio
import logging
from datetime import datetime
import websockets

from ocpp.routing import on, after
from ocpp.v16 import call, call_result
from ocpp.v16 import ChargePoint as cp
from ocpp.v16.enums import *

logging.basicConfig(level=logging.INFO)

class ChargePoint(cp):

    async def main_loop(self):
        global CHARGING
        global TRANSACTION_ID

        CHARGING = False

        while True:
            # Wait for external Authorization request
            id_tag = await self.user_input()

            # Send Authorize.req to the backend, get transaction id
            TRANSACTION_ID = await self.send_authorize(id_tag=id_tag)

            while CHARGING:
                id_tag = await self.user_input()
                if id_tag:
                    TRANSACTION_ID = await self.send_authorize(id_tag=id_tag)
                    break


    async def user_input(self):
        await asyncio.sleep(5)
        id_tag = 'FED4269'
        return id_tag

    async def send_boot_notification(self):
        request = call.BootNotificationPayload(
            charge_point_model="Python",
            charge_point_vendor="Test Script"
        )

        response = await self.call(request)

        if response.status == RegistrationStatus.accepted:
            logging.info("Connected to central system.")
            await self.send_heartbeat()
        elif response.status == RegistrationStatus.rejected:
            logging.info("Central system rejected the connection!")

    async def send_heartbeat(self):
        while True:
            try:
                request = call.HeartbeatPayload()                              
                response = await self.call(request)
                # Heartbeat rate in sec
                await asyncio.sleep(10)
            except:
                raise


    async def send_authorize(self, id_tag: str):
        global CHARGING
        global TRANSACTION_ID

        request = call.AuthorizePayload(
            id_tag=id_tag
        )

        response = await self.call(request)

        if response.id_tag_info["status"] == "Accepted":
            logging.info("Authorization successful")
            if not CHARGING:
                global TRANSACTION_ID
                TRANSACTION_ID = await self.start_transaction(id_tag)
                CHARGING = True
            else:
                await self.stop_transaction(transaction_id=TRANSACTION_ID)
                CHARGING = False
                TRANSACTION_ID = None
            return TRANSACTION_ID

        else:
            logging.info("Authorization unsuccessful")
            return

    async def start_transaction(self, id_tag):
        request = call.StartTransactionPayload(
            connector_id=1,
            id_tag=id_tag,
            meter_start=0,          # Initial Energy meter value / integer
            timestamp=datetime.utcnow().isoformat()
        )

        response = await self.call(request)

        if response.id_tag_info["status"] == "Accepted":
            logging.info("Start Charging ...")
            return response.transaction_id
        else:
            logging.info("Problems with starting the charge process!")
            return

    async def stop_transaction(self, transaction_id):
        request = call.StopTransactionPayload(
            transaction_id=transaction_id,
            meter_stop=1,          # End Energy meter value / integer
            timestamp=datetime.utcnow().isoformat()
        )

        response = await self.call(request)

        # if response.id_tag_info["status"] == "Accepted":
        logging.info("Charging stopped.")
        #     return
        # else:
        #     logging.info("Error in executing StopTransaction!")
        #     return


async def main():
    async with websockets.connect(
        'ws://localhost:9000/CP_3',
        subprotocols=['ocpp1.6']
    ) as ws:

        cp = ChargePoint('CP_3', ws)

        await asyncio.gather(cp.start(), cp.send_boot_notification(), cp.main_loop())


if __name__ == '__main__':
    asyncio.run(main())
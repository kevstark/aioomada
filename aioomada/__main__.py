"""Use aioomada as a CLI."""

import argparse
import asyncio
import logging

import aiohttp
import async_timeout

import aioomada

LOGGER = logging.getLogger(__name__)


def signalling_callback(signal, data):
    """Receive and print events from websocket."""
    LOGGER.info(f"{signal}, {data}")


async def omada_controller(
    host, username, password, port, site, session, sslcontext, callback
):
    """Set up Omada controller and verify credentials."""
    controller = aioomada.Controller(
        host,
        username=username,
        password=password,
        port=port,
        site=site,
        websession=session,
        sslcontext=sslcontext,
        callback=callback,
    )

    try:
        with async_timeout.timeout(10):
            await controller.check_unifi_os()
            await controller.login()
        return controller

    except aioomada.LoginRequired:
        LOGGER.warning(f"Connected to Omada at {host} but couldn't log in")

    except aioomada.Unauthorized:
        LOGGER.warning(f"Connected to Omada at {host} but not registered")

    except (asyncio.TimeoutError, aioomada.RequestError):
        LOGGER.exception(f"Error connecting to the Omada controller at {host}")

    except aioomada.AioOmadaException:
        LOGGER.exception("Unknown Omada communication error occurred")


async def main(host, username, password, port, site, sslcontext=False):
    """CLI method for library."""
    LOGGER.info("Starting aioOmada")

    websession = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))

    controller = await omada_controller(
        host=host,
        username=username,
        password=password,
        port=port,
        site=site,
        session=websession,
        sslcontext=sslcontext,
        callback=signalling_callback,
    )

    if not controller:
        LOGGER.error("Couldn't connect to Omada controller")
        await websession.close()
        return

    await controller.initialize()
    await controller.sites()
    await controller.site_description()
    controller.start_websocket()

    try:
        while True:
            await asyncio.sleep(1)

    except asyncio.CancelledError:
        pass

    finally:
        controller.stop_websocket()
        await websession.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=str)
    parser.add_argument("username", type=str)
    parser.add_argument("password", type=str)
    parser.add_argument("-p", "--port", type=int, default=8043)
    parser.add_argument("-s", "--site", type=str, default="Default")
    parser.add_argument("-D", "--debug", action="store_true")
    args = parser.parse_args()

    loglevel = logging.INFO
    if args.debug:
        loglevel = logging.DEBUG
    logging.basicConfig(format="%(message)s", level=loglevel)

    LOGGER.info(
        f"{args.host}, {args.username}, {args.password}, {args.port}, {args.site}"
    )

    try:
        asyncio.run(
            main(
                host=args.host,
                username=args.username,
                password=args.password,
                port=args.port,
                site=args.site,
            )
        )
    except KeyboardInterrupt:
        pass

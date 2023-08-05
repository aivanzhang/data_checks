from .consistency_suite import ConsistencySuite
import asyncio


ConsistencySuite().run()
# asyncio.run(ConsistencySuite().run_async())


# async def test():
#     runs = await ConsistencySuite().run_async(
#         should_run=False,
#     )
#     await asyncio.gather(*runs)


# asyncio.run(test())

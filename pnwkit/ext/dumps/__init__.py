from .async_ import AsyncData
from .sync import SyncData

request_as_bytes = SyncData.request_as_bytes
request_as_str = SyncData.request_as_str
request_as_csv = SyncData.request_as_csv
request_as_dicts = SyncData.request_as_dicts
request_as_dict = SyncData.request_as_dict
request_as_data = SyncData.request_as_data
request_as_data_dict = SyncData.request_as_data_dict

async_request_as_bytes = AsyncData.request_as_bytes
async_request_as_str = AsyncData.request_as_str
async_request_as_csv = AsyncData.request_as_csv
async_request_as_dicts = AsyncData.request_as_dicts
async_request_as_dict = AsyncData.request_as_dict
async_request_as_data = AsyncData.request_as_data
async_request_as_data_dict = AsyncData.request_as_data_dict

# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: schema.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0cschema.proto\x1a\x1cgoogle/protobuf/struct.proto\"d\n\x04Task\x12\n\n\x02id\x18\x01 \x01(\t\x12\x14\n\x0c\x63ontainerRef\x18\x02 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x03 \x01(\t\x12)\n\x08resource\x18\x04 \x01(\x0b\x32\x17.google.protobuf.Struct\")\n\nTaskResult\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07\x63ontent\x18\x02 \x01(\tb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'schema_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _globals['_TASK']._serialized_start=46
  _globals['_TASK']._serialized_end=146
  _globals['_TASKRESULT']._serialized_start=148
  _globals['_TASKRESULT']._serialized_end=189
# @@protoc_insertion_point(module_scope)
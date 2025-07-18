# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

from akash_api.akash.deployment.v1beta1 import query_pb2 as akash_dot_deployment_dot_v1beta1_dot_query__pb2

GRPC_GENERATED_VERSION = '1.73.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in akash/deployment/v1beta1/query_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )

class QueryStub(object):
    """Query defines the gRPC querier service
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Deployments = channel.unary_unary(
                '/akash.deployment.v1beta1.Query/Deployments',
                request_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsRequest.SerializeToString,
                response_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsResponse.FromString,
                _registered_method=True)
        self.Deployment = channel.unary_unary(
                '/akash.deployment.v1beta1.Query/Deployment',
                request_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentRequest.SerializeToString,
                response_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentResponse.FromString,
                _registered_method=True)
        self.Group = channel.unary_unary(
                '/akash.deployment.v1beta1.Query/Group',
                request_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupRequest.SerializeToString,
                response_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupResponse.FromString,
                _registered_method=True)

class QueryServicer(object):
    """Query defines the gRPC querier service
    """

    def Deployments(self, request, context):
        """Deployments queries deployments
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Deployment(self, request, context):
        """Deployment queries deployment details
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def Group(self, request, context):
        """Group queries group details
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

def add_QueryServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Deployments': grpc.unary_unary_rpc_method_handler(
                    servicer.Deployments,
                    request_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsRequest.FromString,
                    response_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsResponse.SerializeToString,
            ),
            'Deployment': grpc.unary_unary_rpc_method_handler(
                    servicer.Deployment,
                    request_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentRequest.FromString,
                    response_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentResponse.SerializeToString,
            ),
            'Group': grpc.unary_unary_rpc_method_handler(
                    servicer.Group,
                    request_deserializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupRequest.FromString,
                    response_serializer=akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'akash.deployment.v1beta1.Query', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('akash.deployment.v1beta1.Query', rpc_method_handlers)

 # This class is part of an EXPERIMENTAL API.
class Query(object):
    """Query defines the gRPC querier service
    """

    @staticmethod
    def Deployments(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/akash.deployment.v1beta1.Query/Deployments',
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsRequest.SerializeToString,
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Deployment(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/akash.deployment.v1beta1.Query/Deployment',
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentRequest.SerializeToString,
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryDeploymentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def Group(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/akash.deployment.v1beta1.Query/Group',
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupRequest.SerializeToString,
            akash_dot_deployment_dot_v1beta1_dot_query__pb2.QueryGroupResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

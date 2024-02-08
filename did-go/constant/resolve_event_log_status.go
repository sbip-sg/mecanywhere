package constant

type ResolveEventLogStatus int

const (
	RESOLVE_EVENT_LOG_STATUS_SUCCESS       ResolveEventLogStatus = 0
	RESOLVE_EVENT_LOG_STATUS_EVENTLOG_NULL ResolveEventLogStatus = -1
	RESOLVE_EVENT_LOG_STATUS_RES_NULL      ResolveEventLogStatus = -2
	RESOLVE_EVENT_LOG_STATUS_KEY_NOT_MATCH ResolveEventLogStatus = -3
	RESOLVE_EVENT_LOG_STATUS_EVENT_NULL    ResolveEventLogStatus = -4
)

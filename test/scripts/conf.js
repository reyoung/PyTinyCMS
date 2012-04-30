var BASE_URL='http://127.0.0.1:1234'
var REQUEST_VERSION="0.1.0"

function AJAX(method,uri,onSuccess,data,onError){
	$.ajax({
		beforeSend:function(req) {
			req.setRequestHeader('Version',REQUEST_VERSION)
		},
		type:method,
		url:BASE_URL+uri,
		success:onSuccess,
		error:onError,
		dataType:"json",
		data:data
	})
}
function PUT(uri,data,onSuccess,onError){
	AJAX("PUT",uri,onSuccess,data,onError)
}
function DELETE(uri,data,onSuccess,onError){
	AJAX('DELETE',uri,onSuccess,data,onError)
}
function POST(uri,data,onSuccess,onError){
	AJAX('POST',uri,onSuccess,data,onError)
}

// JavaScript Document
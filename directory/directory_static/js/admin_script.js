var Admin = {
    seller_request_decision:function(decision){
	var submit_obj = {"decision":decision};
	var obj = {"value":["seller_request_id"]};
	App.submit_data(obj,submit_obj,"/admin/seller/request/decision", Admin.seller_request_decision_callback, "loader");
    },
    seller_request_decision_callback:function(data){
	window.location.reload();
    }
}
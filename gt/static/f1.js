var gthelp = function () {
	alert('hello,world!')
}

var gtenter = function(){
	alert(jq("#nsrxxForm_nsrsbh").val());
}

jq(document).ready(function () {
	jq("#nsrxxForm_nsrsbh").each(function () {
		var nsr = jq(this)
			nsr.css("width", "80%");
		nsr.parent().append("<br><a id='golabel' href='javascript:void(0)' onclick='gthelp()'>go</a>");
		window.onhelp = new Function("return false;");
		nsr.bind("keyup", function (e) {
			if (e.keyCode == 112 || e.keyCode == 13) {
				gtenter();
			}
		});	
		//jq(document.body).append("<div id=\"_gtool_div\"></div>");
		jq.get("_gtool_/f1dia.html", function (data) {
			//alert(data);
			jq(document.body).append(data);
		});
	});
});

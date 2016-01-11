$(document).ready(function () {
	$(".loginbtn:first").each(function () {
		$(".loginbtn").parent().append("<label><input name='saveuser' id='saveuser' type='checkbox'>保存账号</label>");

		save = store.get("save");
		user = store.get("user");
		//pwd = store.get("pwd");
		if (save) {
			$("#username").val(user);
			//$("#password").val(pwd);
			$("#saveuser").attr("checked", true)
		}

		$("form").submit(function (e) {
			user = $("#username").val();
			pwd = $("#password").val();
			save = $("#saveuser").attr("checked");
			store.set("save", save);
			//store.set("pwd", pwd);
			store.set("user", user);
			//alert(save)
		})
		if (window.navigator.platform != 'Win32') {
			alert("您现在使用的不是32位浏览器，强烈建议您选择32位 Internet Explorer!")
		}
	})
})

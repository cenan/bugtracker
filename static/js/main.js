function decodeQueryParameters() {
	var q = document.location.search,
		params = {},
		token,
		re = /[?&]?([^=]+)=([^&]*)/g;
	q = q.split("+").join(" ");
	while (tokens = re.exec(q)) {
		params[decodeURIComponent(tokens[1])] = decodeURIComponent(tokens[2]);
	}
	return params;
}

function encodeQueryParams(obj) {
	var result = [];
	$.each(obj, function (n, v) {
		result.push(n+"="+encodeURIComponent(v));
	});
	if (result.length) {
		return "?" + result.join("&");
	} else {
		return "";
	}
}

$(function() {
	$('#show_update_pane').click(function() {
		$(this).hide();
		$('.update_issue').animate({height: '100%'}, 2000);
	});
	$("#filelist").tablo({zebraStrip: true});
	$("#version_history").change(function() {
		window.location.href = window.location.origin + window.location.pathname + '?rev=' + $("#version_history").val();
	})
	$("select#category").change(function(e) {
		var default_assignee_id = $("select#category option:selected").data('default_assignee');
		$("select#assignee option[value="+default_assignee_id+"]").attr("selected", "selected");
	});
	$("input[placeholder],textarea[placeholder]").placeholder();
	$(".edit_issue").click(function(e) {
		var title = $("#issue_title").text();
		var content = $("#issue_content").text();
		$("#issue_title").replaceWith('<input id="issue_title" value="'+title+'" /><br />');
		$("#issue_content").replaceWith('<textarea id="issue_content_edit" cols="60" rows="4">'+$.trim(content)+'</textarea><br />');
		$(this).replaceWith('<input type="button" id="save_issue_edit" value="Save" />');
	});
	$("#save_issue_edit").live('click', function(e) {
		var edit_url = "/project/" + $(".issue").data("project-id") + "/edit-issue";
		$.post(edit_url, {issue_id: $("#issue_id").val(), title: $("#issue_title").val(), content: $("#issue_content_edit").val()},
			function(r) {
				window.location.reload();
			}
		);
	});
	$("input[name=milestone]").click(function(e) {
		var mil = [];
		$("input[name=milestone]:checked").each(function (idx, elem) {
			mil.push($(elem).data("milestone-id"));
		});
		qp = decodeQueryParameters();
		qp['mil'] = mil;
		if (mil.length === 0) {
			delete qp['mil'];
		}
		delete qp['p'];
		delete qp['filter'];
		window.location.href = window.location.pathname + encodeQueryParams(qp);
	});
	$("input[name=category]").click(function(e) {
		var cat = [];
		$("input[name=category]:checked").each(function (idx, elem) {
			cat.push($(elem).data("category-id"));
		});
		qp = decodeQueryParameters();
		qp['cat'] = cat;
		if (cat.length === 0) {
			delete qp['cat'];
		}
		delete qp['p'];
		delete qp['filter'];
		window.location.href = window.location.pathname + encodeQueryParams(qp);
	});
	$("input[name=status]").click(function(e) {
		qp = decodeQueryParameters();
		if (($(this).val() != -1) && ($(this).is(':checked'))) {
			qp['status'] = $(this).val();
		} else {
			delete qp['status'];
		}
		delete qp['p'];
		delete qp['filter'];
		window.location.href = window.location.pathname + encodeQueryParams(qp);
	});

	$("#filter-bar li").hover(function () {
		$(".filter-dropdown", this).slideDown(300);
	},
	function () {
		$(".filter-dropdown", this).slideUp(200);
	});
	$("#save-filter").click(function () {
		$(this).text("Saving ...");
		$.post("/user/save-filter/"+document.location.search, function(r) {
			alert(r);
			$("#save-filter").text("Save filter");
		});
	});
});
/*
$(window).load(function() {
	var issue_list_height = $(".issue_list").height() - 10;
	if (issue_list_height > $("#sidebar").height()) {
		$("#sidebar").height(issue_list_height);
	}
});
*/


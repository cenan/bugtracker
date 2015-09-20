(function($) {

$.fn.tablo = function(options) {
	if (options === 'filter') {
		return $.fn.tablo.filter.apply(this, Array.prototype.splice.call(arguments, 1));
	}
	var plugin_options = $.extend({}, $.fn.tablo.defaultOptions, options);
	return this.each(function() {
		var $table = $(this), currentPage,
		sort = function(column_idx, sort_asc) {
			$("th", $table).removeClass('sortasc sortdesc')
			               .eq(column_idx)
			               .addClass((sort_asc?'sortasc':'sortdesc'));
			var rows = [];
			$("tbody>tr", $table).each(function(row_idx, element) {
				rows.push({tr:element,td:$("td", element).eq(column_idx)});
			});
			rows.sort(function(a, b) {
				var r = $(a.td).html() < $(b.td).html() ? -1 : $(a.td).html() > $(b.td).html() ? 1 : 0;
				return sort_asc ? r : r * -1;
			});
			$("tbody>tr", $table).remove();
			$(rows).each(function(idx, row) {
				$("tbody", $table).append(row.tr);
				if (plugin_options.zebraStrip) {
					$("tbody>tr", $table).removeClass("odd").filter(":odd").addClass("odd");
				}
			});
			pager(currentPage);
		},
		pager = function(pageIndex) {
			if (!plugin_options.pager) {
				return;
			}
			$("tbody>tr", $table).hide();
			var items_index = (plugin_options.itemsPerPage * (pageIndex - 1));
			$("tbody>tr", $table).slice(items_index, items_index + plugin_options.itemsPerPage).show();
			currentPage = pageIndex;
		},
		cancelEdit = function() {
			if (!$("#inplacechar").length) {
				return;
			}
			var p = $("#inplacechar").parent();
			$(this).remove();
			p.text(p.data('ovalue'));
		};

		if (plugin_options.pager) {
			for (var i = 0; i < $("tbody>tr", $table).length / plugin_options.itemsPerPage; i++) {
				$("tfoot>tr>td.pagercell", $table).append('<span class="pagenumber">'+(i+1)+'</span>');
			}
			$("tfoot>tr>td.pagercell>span:first-child", $table).addClass("activepagenumber");
			$(".pagenumber").click(function(event) {
				$("tfoot>tr>td.pagercell>span", $table).removeClass("activepagenumber");
				$(this).addClass("activepagenumber");
				pager($(this).text());
			});
			pager(1);
		}
		if (plugin_options.inPlaceEditing) {
			$("tbody>tr>td", $table).live("dblclick", function() {
				if ($("input", this).length) {
					return;
				}
				cancelEdit();
				$(this)
					.data('ovalue', $(this).text())
					.html('<input type="text" id="inplacechar" value="'+$(this).text()+'" />')
					.find('input')
					.bind('focus', function () {
						$(this).css('borderColor', '');
					})
					.bind('blur', function () {
						$(this).css('borderColor', '#f00');
					})
					.focus();
			});
			$("#inplacechar").live('keydown', function(e) {
				if (e.keyCode == 13) {
					e.preventDefault();
					var p = $("#inplacechar").parent(),
						v = $("#inplacechar").val();
					p.text(v);
					if ($.isFunction(plugin_options.inPlaceCallback)) {
						plugin_options.inPlaceCallback(this, p);
					}
					$(this).remove();
				}
				if (e.keyCode == 27) {
					e.preventDefault();
					cancelEdit();
				}
			});
		}
		if (plugin_options.zebraStrip) {
			$("tbody>tr:odd", $table).addClass("odd");
		}
		$("th:not(.nosort)", $table).live('click', function() {
			var column_index = $("th", $table).index(this),
			    sort_asc = true;
			if ($table.data("sort-column") != column_index) {
				$table.data("sort-column", column_index);
			} else {
				sort_asc = !$table.data("sort-order");
			}
			$table.data("sort-order", sort_asc);
			sort(column_index, sort_asc);
		});
	});
};

$.fn.tablo.filter = function(str) {
	var $table = $(this);
	$("tbody>tr", $table).hide();
	$.each($("tbody td", $table), function (idx, elem) {
		if ($(elem).text().indexOf(str) !== -1) {
			$(elem).parent().show();
		}
	});
}

$.fn.tablo.defaultOptions = {
	zebraStrip: false,
	pager: false,
	itemsPerPage: 10,
	inPlaceEditing: false,
	inPlaceCallback: null
};

})(jQuery);

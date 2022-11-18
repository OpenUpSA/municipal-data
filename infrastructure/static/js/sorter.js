var mm = mm || {};
mm.Sorter = mm.Sorter || (function () {
  var Sorter = function (dropdown) {
    this.listeners = {};
    this.state = null;
    this.dropdown = dropdown;
    this.sortOptions = [
      { label: 'Alphabetical (a-z)', value: 'project_description' },
      { label: 'Alphabetical (z-a)', value: '-project_description' },
	    { label: 'Function (descending)', value: '-function' },
      { label: 'Function (ascending)', value: 'function' },
	    { label: 'Project Type (descending)', value: '-project_type' },
      { label: 'Project Type (ascending)', value: 'project_type' },
      { label: 'Value (descending)', value: '-total_forecast_budget' },
      { label: 'Value (ascending)', value: 'total_forecast_budget' },

    ];
  };

  Sorter.prototype = {
    initialize() {
      var me = this;
      var options = this.dropdown.find('nav .dropdown-link');
      me.template = $(options[0]).clone();
      options.remove();

      this.sortOptions.forEach((el) => {
        var option = me.template.clone();
        $('.dropdown-label', option).text(el.label);
        $('.dropdown-label', option).attr('data-option', el.value);
        me.dropdown.find('nav').append(option);
        option.on('click', (e) => {
          var sortField = $('div', option).data('option');
          me.trigger('sortchanged', sortField);
		    $('.sorting-dropdown_trigger .text-block').text(el.label);
		    $('.sorting-dropdown_list').removeClass('w--open');
        });
      });
    },

    on(e, func) {
      if (this.listeners[e] == undefined) this.listeners[e] = [];

      this.listeners[e].push(func);
    },

    trigger(e, payload) {
      for (idx in this.listeners[e]) {
        this.listeners[e][idx](payload);
      }
    },
  };

  return Sorter;
}());

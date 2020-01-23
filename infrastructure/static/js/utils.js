var mm = mm || {}

mm.utils = mm.utils || {
    formatUnits: function(number) {
        if (number >= 10**9) {
            return "bn"
        } else if (number >= 10**6) {
            return "mil"
        }
        return ""
    },

    formatHuman: function(number) {
        if (number >= 10**9) {
            number = number / 10**9
        } else if (number >= 10**6) {
            number = number / 10**6;
        } else {
            return "R" + parseInt(number).toLocaleString();
        }

        return "R" + parseFloat(number).toFixed(1);
    },

    formatNumber: function(number) {
        return parseInt(number).toLocaleString();
    },

    formatCurrency: function(decimalString) {
        if (decimalString == null)
            return "";
        return "R " + Math.round(parseFloat(decimalString)).toLocaleString();
    }
}

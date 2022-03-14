var mm = mm || {};

mm.utils = mm.utils || {
    formatUnits: function(number) {
        if (number >= 10**9) {
            return "billion";
        } else if (number >= 10**6) {
            return "million";
        }
        return "";
    },

    formatHuman: function(number) {
        if (number >= 10**9) {
            number = number / 10**9;
        } else if (number >= 10**6) {
            number = number / 10**6;
        } else {
            return "R" + parseInt(number).toLocaleString();
        }

        return "R" + parseFloat(number).toFixed(1);
    },

    formatNumber: function(number, isFormat=false) {
        if (isFormat) {
            var amount = Humanize.compactInteger(parseInt(number), 2);
            return amount;
        } else {
            return parseInt(number).toLocaleString();
        }
    },

    formatCurrency: function(decimalString) {
        if (decimalString == null)
            return "";
        var value = Humanize.compactInteger(parseFloat(decimalString), 2);
        return "R" + value;
        //return "R " + Math.round(parseFloat(decimalString)).toLocaleString();
    }
};

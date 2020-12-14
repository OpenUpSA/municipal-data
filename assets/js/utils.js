import { formatLocale, format as d3Format } from 'd3-format';

export function logIfUnequal(a, b) {
  if (a !== b) {
    console.error(`${a} !== ${b}`);
  }
}

export const locale = formatLocale({
  decimal: ".",
  thousands: " ",
  grouping: [3],
  currency: ["R", ""],
});

export function capFirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function formatFinancialYear(financialYearEnd) {
  return `${ financialYearEnd - 1 }-${ financialYearEnd }`;
}

export function ratingColor(rating) {
  return {
    "good": "#34A853",
    "ave": "#FBBC05",
    "bad": "#F00",
    "": "#17becf",
  }[rating];
}

export function formatForType(type, value) {
  switch (type) {
  case "%":
    return `${locale.format(".1f")(value)}%`;
  case "R":
    return locale.format("$,")(value);
  case "months":
    return `${locale.format(".1f")(value)} months`;
  case "ratio":
    return locale.format(".2f")(value);
  default:
    console.error(`Don't know how to format for type ${type}`);
    return ""; // Rather show nothing than something that could be misinterpreted
  }
}

export function formatPhase(code) {
  switch (code) {
  case "ORGB": return "Original budget";
  case "ADJB": return "Adjusted budget";
  case "AUDA": return "Audited actual";
  case "ACT": return "Actual";
  case "IBY1": return "Forecast budget";
  case "IBY2": return "Forecast budget";
  default:
    console.error("unknown phase", code);
    return "Phase unknown";
  }
}

export const humaniseRand = (x, longForm) => {
  longForm = longForm === undefined ? true : longForm;
  const randSpace = longForm ? ' ' : '';
  const decimals = 1;
  const suffixBillion = longForm === true ? ' billion' : 'bn';
  const suffixMillion = longForm === true ? ' million' : 'm';
  const suffixThousand = longForm === true ? '  thousand' : 'k';

  if (Math.abs(x) >= 1000000000) {
    return formatRand(x / 1000000000, decimals, randSpace) + suffixBillion;
  } if (Math.abs(x) >= 1000000) {
    return formatRand(x / 1000000, decimals, randSpace) + suffixMillion;
  } if (!longForm && Math.abs(x) >= 100000) {
    return formatRand(x / 1000, decimals, randSpace) + suffixThousand;
  }
  return formatRand(x, 0);
};

const formatRand = (x, decimals, randSpace) => {
  decimals = decimals === undefined ? 1 : decimals;
  randSpace = randSpace === undefined ? ' ' : '';
  return locale.format(`$,.${decimals}f`)(x);
};

export function errorBoundary(f) {
  try {
    f();
  } catch (error) {
    console.error(error);
  }
}

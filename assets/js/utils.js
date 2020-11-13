import { formatLocale } from 'd3-format';

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
    console.warning(`Don't know how to format for type ${type}`);
    return ""; // Rather show nothing than something that could be misinterpreted
  }
}

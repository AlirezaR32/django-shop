export function formatPrice(num) {
  if (num === null || num === undefined) return "—";
  const n = Number(num);
  return n.toLocaleString("fa-IR");
}
export function formatPriceToman(num) {
  return `${formatPrice(num)} تومان`;
}
export function formatOff(price, finalPrice) {
  if (!price || !finalPrice || price === finalPrice) return null;
  const p = (1 - finalPrice / price) * 100;
  return Math.round(p);
}
export function persianNumber(n) {
  return new Intl.NumberFormat("fa-IR").format(n);
}

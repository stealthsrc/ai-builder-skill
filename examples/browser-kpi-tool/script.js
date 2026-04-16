const weeklyData = [
  {
    week: "2026-W14",
    revenue: 48120,
    deals: 19,
    conversion: 0.28,
    regions: [
      { region: "North America", revenue: 24120, deals: 8 },
      { region: "Europe", revenue: 14200, deals: 6 },
      { region: "APAC", revenue: 9800, deals: 5 }
    ]
  },
  {
    week: "2026-W15",
    revenue: 53290,
    deals: 23,
    conversion: 0.31,
    regions: [
      { region: "North America", revenue: 25800, deals: 9 },
      { region: "Europe", revenue: 17140, deals: 8 },
      { region: "APAC", revenue: 10350, deals: 6 }
    ]
  },
  {
    week: "2026-W16",
    revenue: 49840,
    deals: 21,
    conversion: 0.29,
    regions: [
      { region: "North America", revenue: 23720, deals: 8 },
      { region: "Europe", revenue: 15310, deals: 7 },
      { region: "APAC", revenue: 10810, deals: 6 }
    ]
  }
];

const weekSelect = document.querySelector("#week-select");
const revenueValue = document.querySelector("#revenue-value");
const dealsValue = document.querySelector("#deals-value");
const conversionValue = document.querySelector("#conversion-value");
const tableBody = document.querySelector("#region-table-body");

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0
  }).format(value);
}

function populateWeeks() {
  weeklyData.forEach((entry, index) => {
    const option = document.createElement("option");
    option.value = String(index);
    option.textContent = entry.week;
    weekSelect.append(option);
  });
}

function renderWeek(index) {
  const selected = weeklyData[index];
  revenueValue.textContent = formatCurrency(selected.revenue);
  dealsValue.textContent = String(selected.deals);
  conversionValue.textContent = `${Math.round(selected.conversion * 100)}%`;

  tableBody.replaceChildren();

  selected.regions.forEach((row) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${row.region}</td>
      <td>${formatCurrency(row.revenue)}</td>
      <td>${row.deals}</td>
    `;
    tableBody.append(tr);
  });
}

weekSelect.addEventListener("change", (event) => {
  renderWeek(Number(event.target.value));
});

populateWeeks();
renderWeek(weeklyData.length - 1);

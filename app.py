from flask import Flask, jsonify, render_template_string
import json

app = Flask(__name__)

# Sample business analytics data
data = {
    "total_revenue": 412500,
    "units_sold": 1380,
    "avg_order_value": 298.91,
    "monthly": [
        {"month": "Aug", "revenue": 28000},
        {"month": "Sep", "revenue": 34000},
        {"month": "Oct", "revenue": 31000},
        {"month": "Nov", "revenue": 45000},
        {"month": "Dec", "revenue": 52000},
        {"month": "Jan", "revenue": 38000},
        {"month": "Feb", "revenue": 41000},
        {"month": "Mar", "revenue": 36000},
        {"month": "Apr", "revenue": 44000},
        {"month": "May", "revenue": 29000},
        {"month": "Jun", "revenue": 47000},
        {"month": "Jul", "revenue": 50000},
    ],
    "top_products": [
        {"name": "Enterprise Suite", "sales": 98000},
        {"name": "Pro Plan", "sales": 74000},
        {"name": "Starter Pack", "sales": 61000},
        {"name": "Analytics Add-on", "sales": 55000},
        {"name": "Support Bundle", "sales": 43000},
    ]
}

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>📈 Business Analytics Dashboard</title>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Segoe UI', sans-serif; background: #0f172a; color: #e2e8f0; min-height: 100vh; display: flex; overflow-x: hidden; }
    
    /* Layout Containers */
    .sidebar {
      width: 280px;
      height: 100vh;
      background: #0f172a;
      border-right: 1px solid #1e293b;
      position: fixed;
      left: 0;
      top: 0;
      display: flex;
      flex-direction: column;
      z-index: 50;
      box-shadow: 4px 0 24px rgba(0,0,0,0.5);
    }
    .sidebar h2 {
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #475569;
      margin: 24px 24px 8px;
      font-weight: 700;
    }
    .brand {
      padding: 32px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
      border-bottom: 1px solid #1e293b;
    }
    .brand-logo {
      width: 40px;
      height: 40px;
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      box-shadow: 0 4px 12px rgba(37,99,235,0.3);
    }
    .brand-name {
      font-weight: 700;
      font-size: 1.25rem;
      color: #f8fafc;
      letter-spacing: -0.5px;
    }

    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 24px;
      color: #94a3b8;
      text-decoration: none;
      font-size: 0.9rem;
      font-weight: 500;
      transition: all 0.2s ease;
      position: relative;
    }
    .nav-item:hover {
      background: rgba(59, 130, 246, 0.05);
      color: #3b82f6;
    }
    .nav-item.active {
      color: #3b82f6;
      background: rgba(59, 130, 246, 0.1);
    }
    .nav-item.active::before {
      content: '';
      position: absolute;
      left: 0;
      top: 0;
      bottom: 0;
      width: 4px;
      background: #3b82f6;
      border-radius: 0 4px 4px 0;
    }
    .nav-icon {
      font-size: 1.2rem;
    }
    .nav-badge {
      background: #2563eb;
      color: white;
      font-size: 0.65rem;
      padding: 2px 6px;
      border-radius: 12px;
      margin-left: auto;
      font-weight: 700;
      box-shadow: 0 2px 6px rgba(37,99,235,0.4);
    }
    .nav-badge.new {
      background: #10b981;
      box-shadow: 0 2px 6px rgba(16,185,129,0.4);
    }

    .main-content {
      flex: 1;
      margin-left: 280px;
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }

    header {
      background: linear-gradient(135deg, #1e3a5f 0%, #0f172a 100%);
      padding: 24px 40px;
      border-bottom: 2px solid #2563eb;
      display: flex; align-items: center; justify-content: space-between;
    }
    header h1 { font-size: 1.8rem; font-weight: 700; color: #60a5fa; letter-spacing: 0.5px; }
    header span { font-size: 0.85rem; color: #94a3b8; }
    .metrics { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; padding: 32px 40px 0; }
    .card {
      background: #1e293b; border-radius: 12px; padding: 24px;
      border: 1px solid #334155; text-align: center;
      box-shadow: 0 4px 24px rgba(0,0,0,0.3);
      transition: transform 0.2s;
    }
    .card:hover { transform: translateY(-3px); }
    .card h3 { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }
    .card .value { font-size: 2.2rem; font-weight: 800; color: #60a5fa; }
    .charts { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; padding: 24px 40px; }
    .chart-box {
      background: #1e293b; border-radius: 12px; padding: 24px;
      border: 1px solid #334155; box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    .chart-box h2 { font-size: 1rem; color: #cbd5e1; margin-bottom: 18px; font-weight: 600; }
    footer {
      text-align: center; padding: 20px; margin-top: auto;
      color: #475569; font-size: 0.8rem; border-top: 1px solid #1e293b;
    }
    footer span { color: #2563eb; }
  </style>
</head>
<body>
  <aside class="sidebar">
    <div class="brand">
      <div class="brand-logo">📊</div>
      <div class="brand-name">Analytica Pro</div>
    </div>
    
    <nav>
      <h2>Main</h2>
      <a href="#" class="nav-item active">
        <span class="nav-icon">🏠</span>
        <span>Overview</span>
      </a>
      <a href="#" class="nav-item">
        <span class="nav-icon">⚡</span>
        <span>Live Feed</span>
      </a>
      
      <h2>Analytics</h2>
      <a href="#" class="nav-item">
        <span class="nav-icon">💰</span>
        <span>Revenue</span>
      </a>
      <a href="#" class="nav-item">
        <span class="nav-icon">👤</span>
        <span>Customers</span>
      </a>
      <a href="#" class="nav-item">
        <span class="nav-icon">🤖</span>
        <span>AI Insights</span>
        <span class="nav-badge new">NEW</span>
      </a>

      <h2>Management</h2>
      <a href="#" class="nav-item">
        <span class="nav-icon">📦</span>
        <span>Inventory</span>
      </a>
      <a href="#" class="nav-item">
        <span class="nav-icon">👥</span>
        <span>Team</span>
      </a>
      <a href="#" class="nav-item">
        <span class="nav-icon">⚙️</span>
        <span>Settings</span>
      </a>
    </nav>
  </aside>

  <main class="main-content">
    <header>
      <h1>📈 Business Analytics Dashboard</h1>
      <span>Deployed with Docker &nbsp;|&nbsp; Automated with Terraform &amp; Ansible &nbsp;|&nbsp; CI/CD via GitHub Actions</span>
    </header>

    <div class="metrics">
      <div class="card">
        <h3>Total Revenue</h3>
        <div class="value">${{ "{:,}".format(data.total_revenue) }}</div>
      </div>
      <div class="card">
        <h3>Units Sold</h3>
        <div class="value">{{ "{:,}".format(data.units_sold) }}</div>
      </div>
      <div class="card">
        <h3>Avg Order Value</h3>
        <div class="value">${{ "{:.2f}".format(data.avg_order_value) }}</div>
      </div>
    </div>

    <div class="charts">
      <div class="chart-box">
        <h2>Monthly Revenue Trend</h2>
        <canvas id="revenueChart"></canvas>
      </div>
      <div class="chart-box">
        <h2>Top Products by Sales</h2>
        <canvas id="productsChart"></canvas>
      </div>
    </div>

    <footer>
      <span>Business Analytics Dashboard</span> &nbsp;|&nbsp; Automated Cloud Deployment &nbsp;|&nbsp; B9IS121 Assessment
    </footer>
  </main>

  <script>
    const months = {{ months|tojson }};
    const revenues = {{ revenues|tojson }};
    const products = {{ products|tojson }};
    const productSales = {{ product_sales|tojson }};

    new Chart(document.getElementById('revenueChart'), {
      type: 'line',
      data: {
        labels: months,
        datasets: [{
          label: 'Revenue ($)',
          data: revenues,
          borderColor: '#2563eb',
          backgroundColor: 'rgba(37,99,235,0.15)',
          borderWidth: 2,
          fill: true,
          tension: 0.4,
          pointBackgroundColor: '#60a5fa'
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: '#94a3b8' } } },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
          y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
        }
      }
    });

    new Chart(document.getElementById('productsChart'), {
      type: 'bar',
      data: {
        labels: products,
        datasets: [{
          label: 'Sales ($)',
          data: productSales,
          backgroundColor: ['#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe'],
          borderRadius: 6
        }]
      },
      options: {
        responsive: true,
        plugins: { legend: { labels: { color: '#94a3b8' } } },
        scales: {
          x: { ticks: { color: '#94a3b8' }, grid: { color: '#1e293b' } },
          y: { ticks: { color: '#94a3b8' }, grid: { color: '#334155' } }
        }
      }
    });
  </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(
        DASHBOARD_HTML,
        data=type('D', (), data)(),
        months=[m['month'] for m in data['monthly']],
        revenues=[m['revenue'] for m in data['monthly']],
        products=[p['name'] for p in data['top_products']],
        product_sales=[p['sales'] for p in data['top_products']]
    )

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "app": "Business Analytics Dashboard"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)

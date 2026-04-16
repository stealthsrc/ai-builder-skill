# Ruby Patterns

Load this reference when the task requires more than a trivial Ruby script. It provides reusable idioms for CLI tools, file processing, HTTP clients, database access, and common anti-patterns.

Pair with [../builders/ruby-builder.md](../builders/ruby-builder.md) for routing context and with [../rules/security-baseline.md](../rules/security-baseline.md) when the script touches secrets, external APIs, or destructive file operations.

---

## 1. Script Skeleton

```ruby
# frozen_string_literal: true

require 'optparse'
require 'pathname'
require 'logger'

LOG = Logger.new($stdout, progname: File.basename($PROGRAM_NAME, '.rb'))
LOG.formatter = proc { |sev, _, _, msg| "[#{sev}] #{msg}\n" }

OPTIONS = {
  input:   Pathname.new('.'),
  output:  Pathname.new('output.csv'),
  dry_run: false,
  verbose: false
}.freeze

OptionParser.new do |opts|
  opts.banner = "Usage: #{File.basename($PROGRAM_NAME)} [options]"
  opts.on('-i', '--input DIR',    'Input directory')  { |v| OPTIONS[:input]   = Pathname.new(v) }
  opts.on('-o', '--output FILE',  'Output CSV path')  { |v| OPTIONS[:output]  = Pathname.new(v) }
  opts.on('-n', '--dry-run',      'Preview only')     { OPTIONS[:dry_run] = true }
  opts.on('-v', '--verbose',      'Verbose output')   { OPTIONS[:verbose] = true; LOG.level = Logger::DEBUG }
  opts.on('-h', '--help')                             { puts opts; exit }
end.parse!

abort "Input directory not found: #{OPTIONS[:input]}" unless OPTIONS[:input].directory?
```

---

## 2. CSV Read and Write

```ruby
require 'csv'

def read_csv(path)
  CSV.read(path, headers: true, encoding: 'bom|utf-8', strip: true).map(&:to_h)
rescue Errno::ENOENT => e
  abort "Cannot read file: #{e.message}"
end

def write_csv(path, rows, headers:)
  CSV.open(path, 'w', write_headers: true, headers: headers,
           encoding: 'utf-8', write_converters: :all) do |csv|
    rows.each { |row| csv << headers.map { |h| row[h] } }
  end
end
```

---

## 3. HTTP with Net::HTTP and Faraday

```ruby
# Standard library — no gem required for simple GETs
require 'net/http'
require 'uri'
require 'json'

def http_get(url, token:, timeout: 15)
  uri = URI.parse(url)
  http = Net::HTTP.new(uri.host, uri.port)
  http.use_ssl = uri.scheme == 'https'
  http.open_timeout = timeout
  http.read_timeout = timeout

  request = Net::HTTP::Get.new(uri.request_uri)
  request['Authorization'] = "Bearer #{token}"
  request['Accept']        = 'application/json'

  response = http.request(request)
  raise "HTTP #{response.code}: #{response.body[0, 200]}" unless response.is_a?(Net::HTTPSuccess)
  JSON.parse(response.body)
end

# Faraday (gem) — better for retry and middleware
# gem 'faraday', 'faraday-retry'
require 'faraday'
require 'faraday/retry'

def make_client(base_url:, token:)
  Faraday.new(url: base_url) do |f|
    f.request  :json
    f.response :json
    f.request  :retry, max: 3, interval: 1, backoff_factor: 2,
               retry_statuses: [429, 500, 502, 503, 504]
    f.headers['Authorization'] = "Bearer #{token}"
  end
end
```

---

## 4. FileUtils for Safe File Operations

```ruby
require 'fileutils'
require 'pathname'

def safe_move(src, dest_dir, dry_run: false)
  dest_dir = Pathname.new(dest_dir)
  dest     = dest_dir / File.basename(src)

  if dest.exist?
    LOG.warn "Destination exists, skipping: #{dest}"
    return false
  end

  LOG.debug "Move: #{src} → #{dest}"
  return true if dry_run

  FileUtils.mkdir_p(dest_dir)
  FileUtils.mv(src.to_s, dest.to_s)
  true
rescue SystemCallError => e
  LOG.error "Move failed (#{src}): #{e.message}"
  false
end
```

---

## 5. SQLite with Parameterized Queries

```ruby
# gem 'sqlite3'
require 'sqlite3'

def open_db(path)
  db = SQLite3::Database.new(path)
  db.results_as_hash = true
  db.execute('PRAGMA journal_mode = WAL')
  db
end

def find_by_region(db, region)
  # ✓ Parameterized — never string interpolation
  db.execute('SELECT id, region, amount FROM orders WHERE region = ?', [region])
end

# ✗ Never:
# db.execute("SELECT * FROM orders WHERE region = '#{region}'")
```

---

## 6. Environment Secrets

```ruby
def require_env(name)
  value = ENV.fetch(name, nil)
  abort "Missing required environment variable: #{name}" if value.nil? || value.empty?
  value
end

API_KEY  = require_env('API_KEY')
BASE_URL = require_env('BASE_URL')
```

---

## 7. Anti-Patterns

| Anti-pattern | Problem | Fix |
|---|---|---|
| Missing `frozen_string_literal: true` | Unnecessary string allocations | Add to every file |
| `rescue Exception` | Catches `Interrupt` and `SystemExit` | Rescue `StandardError` or specific classes |
| `eval` with user input | Arbitrary code execution | Parse explicitly |
| `system("cmd #{user_input}")` | Shell injection | `system('cmd', user_input)` with array form |
| `File.read(user_path)` without validation | Path traversal | `File.expand_path` + prefix check |
| String interpolation in SQL | SQL injection | Parameterized queries |
| `puts` for logging | No levels, cannot redirect | `Logger` |
| Mutable constant (constant assigned a mutable object) | State leak across calls | `freeze` arrays and hashes assigned to constants |

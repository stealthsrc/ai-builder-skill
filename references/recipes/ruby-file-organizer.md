# Recipe: Ruby File Organizer by Date

Complete Ruby script that organizes files in a source folder into `YYYY/MM/` subdirectories based on the file's last-modified date, with dry-run support, a move log CSV, and collision protection.

Pair with [../builders/ruby-builder.md](../builders/ruby-builder.md) and [../patterns/ruby-patterns.md](../patterns/ruby-patterns.md).

---

## What It Does

1. Scans a source directory for files matching an optional extension filter.
2. Reads each file's last-modified timestamp.
3. Moves each file into `archive/YYYY/MM/filename` — creating directories as needed.
4. Skips files when a collision would occur (same name in the destination).
5. Writes a `move-log-YYYYMMDDHHMMSS.csv` for rollback.
6. Supports `--dry-run` to preview without moving anything.

---

## Gemfile

```ruby
# frozen_string_literal: true

source "https://rubygems.org"
ruby "~> 3.2"

# No gems required — uses stdlib only (optparse, fileutils, csv, logger)
```

---

## organize.rb

```ruby
# frozen_string_literal: true

require 'optparse'
require 'fileutils'
require 'pathname'
require 'csv'
require 'logger'
require 'time'

# ---- Logging ----
LOG = Logger.new($stdout, progname: 'organize')
LOG.formatter = proc { |sev, _, _, msg| "[#{sev[0]}] #{msg}\n" }

# ---- Options ----
options = {
  source:    Pathname.new('.'),
  archive:   Pathname.new('archive'),
  extension: nil,
  dry_run:   false,
  verbose:   false
}

OptionParser.new do |opts|
  opts.banner = "Usage: ruby organize.rb [options]"
  opts.on('-s DIR',  '--source DIR',    'Source directory')     { |v| options[:source]    = Pathname.new(v) }
  opts.on('-a DIR',  '--archive DIR',   'Archive root')         { |v| options[:archive]   = Pathname.new(v) }
  opts.on('-e EXT',  '--extension EXT', 'Filter by extension')  { |v| options[:extension] = v.delete_prefix('.').downcase }
  opts.on('-n',      '--dry-run',       'Preview only')         { options[:dry_run] = true }
  opts.on('-v',      '--verbose')                               { options[:verbose] = true; LOG.level = Logger::DEBUG }
  opts.on('-h',      '--help')                                  { puts opts; exit }
end.parse!

abort "Source directory not found: #{options[:source]}" unless options[:source].directory?

options[:archive].mkpath unless options[:dry_run]

# ---- Build file list ----
files = options[:source].children.select do |path|
  next false unless path.file?
  next true  if options[:extension].nil?
  path.extname.delete_prefix('.').downcase == options[:extension]
end

if files.empty?
  LOG.info "No files found in #{options[:source]}"
  exit 0
end

LOG.info "Found #{files.size} file(s) to process"

# ---- Move log ----
timestamp  = Time.now.strftime('%Y%m%d%H%M%S')
log_path   = options[:archive] / "move-log-#{timestamp}.csv"
log_rows   = [['source', 'destination', 'moved_at']]

moved = skipped = failed = 0

files.each do |src|
  mtime    = src.mtime
  dest_dir = options[:archive] / mtime.strftime('%Y') / mtime.strftime('%m')
  dest     = dest_dir / src.basename

  if dest.exist?
    LOG.warn "Destination exists, skipping: #{dest}"
    skipped += 1
    next
  end

  LOG.debug "Move: #{src} → #{dest}"

  if options[:dry_run]
    puts "[DRY-RUN] #{src.basename} → #{dest}"
    next
  end

  begin
    dest_dir.mkpath
    FileUtils.mv(src.to_s, dest.to_s)
    log_rows << [src.to_s, dest.to_s, Time.now.utc.iso8601]
    moved += 1
  rescue SystemCallError => e
    LOG.error "Move failed (#{src.basename}): #{e.message}"
    failed += 1
  end
end

# ---- Write log ----
unless options[:dry_run] || log_rows.size == 1
  CSV.open(log_path, 'w', write_headers: true, headers: log_rows.first) do |csv|
    log_rows[1..].each { |row| csv << row }
  end
  LOG.info "Move log: #{log_path}"
end

# ---- Summary ----
if options[:dry_run]
  puts "\n[DRY-RUN] No files moved."
else
  LOG.info "Done — moved: #{moved}, skipped: #{skipped}, failed: #{failed}"
end

exit(failed > 0 ? 1 : 0)
```

---

## Run

```bash
# Install (no gems needed — stdlib only)
ruby -e "puts RUBY_VERSION"  # ensure 3.2+

# Dry run — preview
ruby organize.rb --source data/exports --archive data/archive --extension pdf --dry-run

# Live run — move PDFs
ruby organize.rb --source data/exports --archive data/archive --extension pdf --verbose

# All file types
ruby organize.rb --source data/exports --archive data/archive
```

---

## Validation

- Check `archive/YYYY/MM/` directories contain the expected files.
- Open `archive/move-log-YYYYMMDDHHMMSS.csv` — each row has source, destination, and timestamp.
- Verify source directory contains only files that were skipped (collisions) or failed.

---

## Rollback

```bash
# Read the move log and reverse each move
ruby -r csv -r fileutils -e '
  log = ARGV[0] or abort "Usage: ruby -e \"...\" move-log.csv"
  CSV.foreach(log, headers: true) do |row|
    src, dest = row["source"], row["destination"]
    if File.exist?(dest)
      FileUtils.mkdir_p(File.dirname(src))
      FileUtils.mv(dest, src)
      puts "Restored: #{src}"
    else
      warn "Not found: #{dest}"
    end
  end
' archive/move-log-YYYYMMDDHHMMSS.csv
```

---

## Edge Cases

| Case | Behavior |
|---|---|
| Destination file exists | Skips with a warning — never overwrites |
| Source directory has subdirectories | Only processes top-level files (`children.select(&:file?)`) |
| Filename with spaces | Handled natively by Pathname and FileUtils |
| Failed move | Logged, counted, exit code 1 |

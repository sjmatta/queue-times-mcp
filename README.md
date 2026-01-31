# Queue Times MCP Server

An MCP (Model Context Protocol) server that provides real-time theme park wait times from [Queue-Times.com](https://queue-times.com).

## Features

- Get current wait times for individual parks by name or ID
- List all available parks with their IDs and operator groups
- Fetch wait times for all parks in a group (Disney, Universal, SeaWorld, etc.)
- Case-insensitive partial matching for park names

## Installation

```bash
uv sync
```

## Usage

### Run the MCP Server

```bash
uv run poe serve
```

### Development Mode

```bash
uv run poe dev
```

### Available Tools

| Tool | Description |
|------|-------------|
| `list_parks` | List all available theme parks with IDs and groups |
| `get_wait_times` | Get wait times by park name (supports partial matching) |
| `get_wait_times_by_id` | Get wait times by queue-times.com park ID |
| `get_all_wait_times` | Get wait times for all parks in a group |

### Example

```
> get_wait_times("Kennywood")

{
  "park": "Kennywood",
  "lands": [
    {
      "name": "Main Area",
      "rides": [
        {"name": "Steel Curtain", "wait_time": 45, "is_open": true},
        {"name": "Phantom's Revenge", "wait_time": 30, "is_open": true}
      ]
    }
  ]
}
```

## Development

```bash
# Run linting and type checking
uv run poe check

# Run tests
uv run poe test

# Format code
uv run poe format
```

## Attribution

This project uses data from [Queue-Times.com](https://queue-times.com).

**Powered by [Queue-Times.com](https://queue-times.com)**

Per their API terms, applications using this data must display prominent attribution linking back to Queue-Times.com.

## License

MIT License - see [LICENSE](LICENSE) for details.

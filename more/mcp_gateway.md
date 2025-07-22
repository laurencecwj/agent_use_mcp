# 使用mcp gateway来统一所有的mcp server

其实不推荐，在proxy上有可能会导致result的json化和json string化的混乱，实际上在跑的过程里面出现了mcp结果到mcp-agent这边识别混乱的问题，如果一定要解决应该是可以行得通的，但是个人感觉意义不大。

所以如下的仅供参考，它们只解决了技术路径上的可行性。

## 开源项目: 

#### mcp-hub

https://github.com/ravitemer/mcp-hub

可以在当前目录下：

```bash
npm install mcp-hub
```

#### mcptools

https://github.com/f/mcptools

可以先

git clone https://github.com/f/mcptools

然后在mcptools目录下

```bash
go build -o mcp main.go

ls -l
# 可以看到mcp这个新增的binary
-rwxr-xr-x 1 laurence laurence 12953565 Jul 22 06:49 mcp
```

## 使用方法

### 1. 增加配置文件 mcp.json
```json
{
  "mcpServers": {
    "fs": {
       "url": "http://10.148.0.8:8989/mcp"
    },
    "pandas": {
       "url": "http://10.148.0.8:8100/sse"
    }
  }
}
```

### 2. 启动mcp-hub
```bash
node_modules/.bin/mcp-hub --port 3000 --config ./mcp.json
```

### 3. 利用mcptool来验证mcp服务

```bash
./mcp tools --transport sse http://localhost:3000/mcp

# 将会看到类似这样的输出
fs__create_directory(path:str)
     Create a new directory or ensure a directory exists. Can create multiple nested directories in one operation. If the directory already exists, this
     operation will succeed silently. Perfect for setting up directory structures for projects or ensuring required paths exist. Only works within allowed
     directories.

fs__delete_file(path:str)
     Delete file or directory

fs__directory_tree(path:str)
     Get a recursive tree view of files and directories as a JSON structure. Each entry includes 'name', 'type' (file/directory), and 'children' for directories.
     Files have no children array, while directories always have a children array (which may be empty). The output is formatted with 2-space indentation for
     readability. Only works within allowed directories.

fs__edit_file(path:str, [dryRun:bool], [edits:str[]])
     Make line-based edits to a text file. Each edit replaces exact line sequences with new content. Returns a git-style diff showing the changes made. Only
     works within allowed directories.

fs__get_file_info(path:str)
     Retrieve detailed metadata about a file or directory. Returns comprehensive information including size, creation time, last modified time, permissions, and
     type. This tool is perfect for understanding file characteristics without reading the actual content. Only works within allowed directories.

fs__list_allowed_directories
     Returns the list of directories that this server is allowed to access. Use this to understand which directories are available before trying to access files.

fs__list_directory(path:str)
     Get a detailed listing of all files and directories in a specified path. Results clearly distinguish between files and directories with [FILE] and [DIR]
     prefixes. This tool is essential for understanding directory structure and finding specific files within a directory. Only works within allowed directories.

fs__list_directory_with_sizes(path:str, [sortBy:str])
     Get a detailed listing of all files and directories in a specified path, including sizes. Results clearly distinguish between files and directories with
     [FILE] and [DIR] prefixes. This tool is useful for understanding directory structure and finding specific files within a directory. Only works within
     allowed directories.

fs__move_file(destination:str, source:str)
     Move or rename files and directories. Can move files between directories and rename them in a single operation. If the destination exists, the operation
     will fail. Works across different directories and can be used for simple renaming within the same directory. Both source and destination must be within
     allowed directories.

fs__read_file(path:str)
     Read the complete contents of a file from the file system. Handles various text encodings and provides detailed error messages if the file cannot be read.
     Use this tool when you need to examine the contents of a single file. Use the 'head' parameter to read only the first N lines of a file, or the 'tail'
     parameter to read only the last N lines of a file. Only works within allowed directories.

fs__read_multiple_files([paths:str[]])
     Read the contents of multiple files simultaneously. This is more efficient than reading files one by one when you need to analyze or compare multiple files.
     Each file's content is returned with its path as a reference. Failed reads for individual files won't stop the entire operation. Only works within allowed
     directories.

fs__search_files(path:str, pattern:str, [excludePatterns:str[]])
     Recursively search for files and directories matching a pattern. Searches through all subdirectories from the starting path. The search is case-insensitive
     and matches partial names. Returns full paths to all matching items. Great for finding files when you don't know their exact location. Only searches within
     allowed directories.

fs__write_file(content:str, path:str)
     Create a new file or completely overwrite an existing file with new content. Use with caution as it will overwrite existing files without warning. Handles
     text content with proper encoding. Only works within allowed directories.

pandas__read_metadata_tool(file_path:str)
     Read file metadata (Excel or CSV) and return in MCP-compatible format. Args: file_path: Absolute path to data file Returns: dict: Structured metadata
     including: For Excel: - file_info: {type: "excel", sheet_count, sheet_names} - data: {sheets: [{sheet_name, rows, columns}]} For CSV: - file_info: {type:
     "csv", encoding, delimiter} - data: {rows, columns} Common: - status: SUCCESS/ERROR - columns contain: - name, type, examples - stats: null_count,
     unique_count - warnings, suggested_operations

pandas__run_pandas_code_tool(code:str)
     Execute pandas code with smart suggestions and security checks. Args: code: Python code string containing pandas operations Returns: dict: Either the result
     or error information

pandas__generate_chartjs_tool(data:obj, [chart_types:arr], [request_params:obj], [title:str])
     Generate interactive Chart.js visualizations from structured data. Args: data: Structured data in MCP format with required structure: { "columns": [ {
     "name": str, # Column name "type": str, # "string" or "number" "examples": list # Array of values }, ... # Additional columns ] } Example: { "columns": [ {
     "name": "Category", "type": "string", "examples": ["A", "B", "C"] }, { "name": "Value", "type": "number", "examples": [10, 20, 30] } ] } chart_types: List
     of supported chart types to generate (first is used) title: Chart title string request_params: Additional visualization parameters (optional) Returns: dict:
     Result with structure: { "status": "SUCCESS"|"ERROR", "chart_html": str, # Generated HTML content "chart_type": str, # Type of chart generated "html_path":
     str # Path to saved HTML file }     
```
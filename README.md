# panda-patrol

### WIP
[x] suites
[ ] GE integration


[ ] roadmap
### Lower Priority
[ ] Download and store locally
```python
    @classmethod
    def init(cls, file_path: str) -> "Check":
        """
        Initialize a check from a JSON file
        """
        return cls()

    def save_to_file(self, file_path: str):
        """
        Save the check to a file
        """
        return
```
[ ] rules_context without decorator (with comments)
[ ] streaming database
[ ] anomaly detection
[ ] pretty printing
[ ] frontend
[ ] data profiling
[ ] deployment
[ ] wrap assertions for printing
- Go from notebook to check
    [ ] check.init => name, etc
    [ ] rule.start() => rule.end()
    [ ] generate_base_file(overwrite)
- @params, ingestor (caching)
- pause check
- depends on pipeline
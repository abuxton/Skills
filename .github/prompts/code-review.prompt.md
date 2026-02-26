# Code Review Helper

Review the selected code or the changes in this pull request.

## Review Scope

[PASTE CODE OR DESCRIBE THE PR/CHANGE TO REVIEW]

## Review Checklist

Please evaluate the code against these criteria and provide specific, actionable feedback:

### Correctness

- [ ] Logic is correct and handles edge cases
- [ ] Error handling is appropriate and consistent
- [ ] No off-by-one errors or boundary condition issues
- [ ] Concurrent/async code is safe from race conditions

### Security

- [ ] No secrets, tokens, or credentials hardcoded
- [ ] Input is validated and sanitised before use
- [ ] No SQL injection, path traversal, or injection vulnerabilities
- [ ] Dependencies are pinned to known-good versions

### Readability & Maintainability

- [ ] Names are clear and self-documenting
- [ ] Functions/methods are small and focused
- [ ] No dead code or commented-out blocks
- [ ] Complex logic has explanatory comments

### Testing

- [ ] New functionality has tests
- [ ] Tests cover edge cases and error paths
- [ ] Tests are independent and not order-dependent

### Performance

- [ ] No obvious N+1 query patterns
- [ ] Large data sets handled with pagination or streaming
- [ ] No unnecessary computation in hot paths

### Git / PR Hygiene

- [ ] Commits follow conventional commit format
- [ ] PR is small and focused (one concern)
- [ ] No unrelated changes mixed in

## Output Format

For each issue found, provide:

1. **Severity**: `blocking` | `suggestion` | `nit`
2. **Location**: file and line reference
3. **Issue**: what is wrong or could be improved
4. **Recommendation**: the specific change to make

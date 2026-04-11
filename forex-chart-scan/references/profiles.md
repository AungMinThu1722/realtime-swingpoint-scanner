# Seek and Destroy Scan Rules

## Candle pattern
Compare candle2 against candle1 (previous candle).

### Required conditions
- candle2.high > candle1.high + tolerance
- candle2.low < candle1.low - tolerance
- (candle2.high - candle1.high) > min_sweep
- (candle1.low - candle2.low) > min_sweep
- candle2.close is inside candle1 range:
  - candle1.low <= candle2.close <= candle1.high

### Output
- Boolean Series aligned to the input index
- First row must be False
- No loops if vectorized pandas logic is available

## Aim For Range Low

Two-candle bullish sweep profile.

Rules:
- c2.high > c1.high
- c1.low <= c2.close <= c1.high
- (c2.high - c1.high) > min_sweep

Interpretation:
- aim bias is down
- target is c1.low

## Aim For Range High

Vice versa of Aim For Range Low.

Rules:
- c2.low < c1.low
- c1.low <= c2.close <= c1.high
- (c1.low - c2.low) > min_sweep

Interpretation:
- aim bias is up
- target is c1.high

### Ongoing candle handling
- Do not evaluate the most recent unfinished candle when user requests it.
- Prefer caller-controlled trimming (e.g. df.iloc[:-1] or df.iloc[:-2]).

### Defaults
- tolerance = 0.0
- min_sweep = 0.0

### Data expectations
- pandas DataFrame with columns:
  - open
  - high
  - low
  - close
  - volume
- Clean column names to lowercase before processing.

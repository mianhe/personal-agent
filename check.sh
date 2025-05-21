#!/bin/sh

echo "🔍 Running code checks..."

# 检查 Python 文件格式
echo "\n📝 Running black..."
black --check src/ tests/
if [ $? -ne 0 ]; then
    echo "❌ black check failed. Please run 'black .' to format your code"
    exit 1
fi

# 运行 pylint
echo "\n🔎 Running pylint..."
pylint src/ tests/
if [ $? -ne 0 ]; then
    echo "❌ pylint check failed"
    exit 1
fi

# 运行测试
echo "\n🧪 Running tests..."
python -m pytest -m smoke -v
if [ $? -ne 0 ]; then
    echo "❌ tests failed"
    exit 1
fi

echo "\n✅ All checks passed!"
exit 0 
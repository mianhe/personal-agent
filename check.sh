#!/bin/sh

echo "🔍 Running code checks..."

# 检查 Python 文件格式
echo "\n📝 Running black..."
black --check src/ req_and_test/
if [ $? -ne 0 ]; then
    echo "❌ black check failed. Please run 'black .' to format your code"
    exit 1
fi

# 运行 pylint
echo "\n🔎 Running pylint..."
pylint src/ req_and_test/
if [ $? -ne 0 ]; then
    echo "❌ pylint check failed"
    exit 1
fi

# 运行测试
echo "\n🧪 Running tests..."
python -m pytest req_and_test/acceptance/test_cli_basic.py -v
if [ $? -ne 0 ]; then
    echo "❌ tests failed"
    exit 1
fi

echo "\n✅ All checks passed!"
exit 0 
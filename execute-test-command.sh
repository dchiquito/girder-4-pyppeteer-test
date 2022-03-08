# Install the project
cd $GITHUB_WORKSPACE
echo "Navigating to $INPUT_INSTALL_DIRECTORY"
cd $INPUT_INSTALL_DIRECTORY
echo "Installing with $INPUT_INSTALL_COMMAND"
$INPUT_INSTALL_COMMAND

# Log versions for debugging
echo "node version: $(node --version)"
echo "npm version: $(npm --version)"
echo "yarn version: $(yarn --version)"
echo "vue version: $(vue --version)"

# Run the pyppeteer tests
cd $GITHUB_WORKSPACE
echo "Navigating to $INPUT_TEST_DIRECTORY"
cd $INPUT_TEST_DIRECTORY
echo "Running tests with $INPUT_TEST_COMMAND"
$INPUT_TEST_COMMAND

echo "Navigating to $INPUT_WORKING_DIRECTORY"
cd $INPUT_WORKING_DIRECTORY
echo "Installing with $INPUT_INSTALL_COMMAND"
$INPUT_INSTALL_COMMAND
echo "Doing git stuff"
pwd
ls
cd $GITHUB_WORKSPACE
pwd
ls
echo "Running tests with $INPUT_TEST_COMMAND"
$INPUT_TEST_COMMAND
echo "Complete!"
echo "Doing git stuff"
cd $GITHUB_WORKSPACE
echo "Navigating to $INPUT_WORKING_DIRECTORY"
cd $INPUT_WORKING_DIRECTORY
echo "Installing with $INPUT_INSTALL_COMMAND"
$INPUT_INSTALL_COMMAND
echo "Currently in:"
pwd
echo "Contents:"
ls
echo "Running tests with $INPUT_TEST_COMMAND"
$INPUT_TEST_COMMAND
echo "Complete!"
echo "Navigating to $WORKING_DIRECTORY"
cd $WORKING_DIRECTORY
echo "Installing with $INSTALL_COMMAND"
$INSTALL_COMMAND
echo "Running tests with $TEST_COMMAND"
$TEST_COMMAND
echo "Complete!"
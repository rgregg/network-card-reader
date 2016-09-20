# Card Reader SharePoint Sample App

This sample application uses the SharePoint Graph API to record badge scans to a SharePoint List.

## Dependencies

This sample targets Python2. 

You can install the latest Python builds from [python.org](https://www.python.org/downloads/).

After installing, you may need to add the python installation directory to your path.

This sample has a few dependencies that must be installed before the script can be run.
Depending on your python configuration, you may need to install additional modules.

The following wheels/eggs must be installed:

* requests
* evdev

To install these, use `pip install <wheel_name>`.


## Setting up the sample

Before you can use the sample, you need to configure an application within your Azure organization.

1. Open the [Azure Management Portal](https://manage.windowsazure.com) and navigate to your Active Directory.
2. Select **Applications** and then click **Add**, and then **Add an application my organization is developing**.
3. Enter a name for your app, like `Card Reader Sample` and select **Native Client Application** and click the next button.
4. For the redirect URI, type in `https://localhost:44399` and click next.
5. Select **Configure** and record the **Client ID** value.
6. Click **Add application** and select **Microsoft Graph** and click the OK button.

After registering your application, copy the details of the app into a copy of **config.template.json** and name the file **config.json**.

## License

See [License](LICENSE.md) for details.
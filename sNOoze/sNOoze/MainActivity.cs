using Android.App;
using Android.Widget;
using Android.OS;
using Android.Bluetooth;
using Android.Content;
using System.Linq;
using System.Text;
//using Xamarin.Forms;

namespace sNOoze
{
    [Activity(Label = "sNOoze", MainLauncher = true, Icon = "@mipmap/icon")]
    public class MainActivity : Activity
    {
        private TimePicker timePicker;
        private Button button;
        private TextView text;

        BluetoothAdapter adapter;
        BluetoothDevice device;
        BluetoothSocket socket;


        protected override void OnCreate(Bundle savedInstanceState)
        {
            base.OnCreate(savedInstanceState);

            // Set our view from the "main" layout resource
            SetContentView(Resource.Layout.Main);

            FindViews();

            // Get our button from the layout resource,
            // and attach an event to it
            SetupButton();
            SetupClock();
            SetupText();


            //bluetooth
            //create socket
            adapter = BluetoothAdapter.DefaultAdapter;
            if (adapter == null) throw new System.Exception("No Bluetooth adapter found.");

            if (!adapter.IsEnabled) throw new System.Exception("Bluetooth adapter is not enabled.");

            //find device
            string deviceHardwareAdd = "";
            device = (from bd in adapter.BondedDevices //paired devices
                      where bd.Name == "raspberrypi"
                      select bd).FirstOrDefault();
            deviceHardwareAdd = device.Address;

            //get socket over this id
            socket = device.CreateRfcommSocketToServiceRecord(Java.Util.UUID.FromString("a60ddd90-0623-11ea-aaef-0800200c9a66"));//B8:27:EB:EC:15:9E

            //asynchronously connect bluetooth
            AsyncConnectBT();

            //On a button click, set alarm
            button.Click += delegate 
            {
                //button.Text = timePicker.Hour.ToString() + " " + timePicker.Minute.ToString();

                SetAlarm(timePicker.Hour, timePicker.Minute);
            };

        }

        private void FindViews()
        {
            text = FindViewById<TextView>(Resource.Id.textView1);
            timePicker = FindViewById<TimePicker>(Resource.Id.timePicker1);
            button = FindViewById<Button>(Resource.Id.myButton);
        }

        /// <summary>
        /// This will access bluetooth and attempt to set alarm.
        /// Will produce alert depending on success/failure.
        /// </summary>
        private void SetAlarm(int hour, int minute)
        {
            //Extract string
            string minuteString = minute.ToString();
            if (minuteString.Length < 2) minuteString = "0" + minuteString;
            string hourString = hour.ToString();
            if (hourString.Length < 2) hourString = "0" + hourString;


            //Set alarm (replace with bluetooth)
            bool success = true;
            text.Text = "current alarm = " + hourString + minuteString;


            //If socket is connected send the bytes
            if(socket.IsConnected)
            {
                byte[] bytesToSend = Encoding.ASCII.GetBytes((hourString + minuteString));
                //SEND TIME HERE
                // Read data from the device
                //await _socket.InputStream.ReadAsync(buffer, 0, buffer.Length);

                // Write data to the device
                //await socket.OutputStream.WriteAsync(buffer, 0, buffer.Length);
                AsyncWriteBT(bytesToSend);
            }
            //if not connected, fail
            else
            {
                success = false;
            }

            //https://brianpeek.com/connect-to-a-bluetooth-device-with-xamarinandroid/


            //Toast popup
            Toast toast;
            string toastString;

            if (success) toastString = "Set alarm to " + hourString + ":" + minuteString;
            else         toastString = "Failed. Check if bluetooth is connected to mattress.";
            toast = Toast.MakeText(this.ApplicationContext, toastString, ToastLength.Short);
            toast.Show();
        }

        private void SetupClock()
        {
            timePicker.SetIs24HourView(Java.Lang.Boolean.True);
        }

        private void SetupButton()
        {
            button.Text = "Set Alarm";
        }

        private void SetupText()
        {
            text.Text = "Current alarm: ???";
        }



        async void AsyncConnectBT()
        {
            await socket.ConnectAsync();
        }

        async void AsyncWriteBT(byte[] buffer)
        {
            await socket.OutputStream.WriteAsync(buffer, 0, buffer.Length);
        }



    }
}


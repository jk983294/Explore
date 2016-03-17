package com.victor.myawesomeapp;

import android.content.ContentValues;
import android.content.Context;
import android.content.Intent;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.EditText;

public class MainActivity extends AppCompatActivity {

    public final static String EXTRA_MESSAGE = "com.victor.myawesomeapp.MESSAGE";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
        fab.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    /** Called when the user clicks the Send button */
    public void sendMessage(View view) {
        Intent intent = new Intent(this, DisplayMessageActivity.class);
        EditText editText = (EditText) findViewById(R.id.edit_message);
        String message = editText.getText().toString();
        intent.putExtra(EXTRA_MESSAGE, message);
        startActivity(intent);
    }

    /**
     * activity is sometimes obstructed by other visual components that cause the activity to pause
     * 1. Stop animations or other ongoing actions that could consume CPU.
     * 2. Commit unsaved changes, but only if users expect such changes to be permanently saved when they leave (such as a draft email).
     * 3. Release system resources, such as broadcast receivers, handles to sensors (like GPS),
     * or any resources that may affect battery life while your activity is paused and the user does not need them.
     *
     * avoid performing CPU-intensive work, such as writing to a database
     */
    @Override
    public void onPause() {
        super.onPause();  // Always call the superclass method first
    }

    /**
     * system calls this method every time your activity comes into the foreground, including when it's created for the first time.
     */
    @Override
    public void onResume() {
        super.onResume();  // Always call the superclass method first
    }

    /**
     * it's no longer visible and should release almost all resources that aren't needed while the user is not using it
     * perform larger, more CPU intensive shut-down operations, such as writing information to a database.
     */
    @Override
    protected void onStop() {
        super.onStop();  // Always call the superclass method first
        // Save the note's current draft, because the activity is stopping and we want to be sure the current note progress isn't lost.
//        ContentValues values = new ContentValues();
//        values.put("COLUMN_NAME_NOTE", "value");
//        getContentResolver().update(uri, values, null, null);
    }

    @Override
    protected void onStart() {
        super.onStart();  // Always call the superclass method first
        // The activity is either being restarted or started for the first time
        // so this is where we should make sure that GPS is enabled
        LocationManager locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        boolean gpsEnabled = locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER);
        if (!gpsEnabled) {
            // Create a dialog here that requests the user to enable GPS, and use an intent with the android.provider.Settings.ACTION_LOCATION_SOURCE_SETTINGS action to take the user to the Settings screen to enable GPS when they click "OK"
        }
    }

    /**
     * onRestart() also calls the onStart() method, which happens every time your activity becomes visible
     */
    @Override
    protected void onRestart() {
        super.onRestart();  // Always call the superclass method first
        // Activity being restarted from stopped state
    }

    /**
     * kill background threads that you created during onCreate() or other long-running resources
     */
    @Override
    public void onDestroy() {
        super.onDestroy();  // Always call the superclass
    }
}

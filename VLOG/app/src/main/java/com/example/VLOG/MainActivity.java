package com.example.khuthon2;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;
import androidx.core.app.ActivityCompat;

import android.Manifest;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.media.Image;
import android.media.MediaPlayer;
import android.net.Uri;
import android.os.Build;
import android.os.Bundle;
import android.os.health.SystemHealthManager;
import android.view.View;
import android.webkit.MimeTypeMap;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.VideoView;

import com.bumptech.glide.Glide;
import com.nbsp.materialfilepicker.MaterialFilePicker;
import com.nbsp.materialfilepicker.ui.FilePickerActivity;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.net.Socket;



public class MainActivity extends AppCompatActivity {
    private Button button;
    private Button videoButton;
    private TextView textView;
    private EditText editText;
    private VideoView videoView;
    private TextView textView2;

    private File f;
    private Socket clientSocket;
    private static final int serverPort = 8080;
    private static final String serverIP = "172.16.28.150";
    private BufferedReader networkReader;
    private BufferedWriter networkWriter;


    AwsConnector awsConnector;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        awsConnector = new AwsConnector();
        awsConnector.initializeAwsS3(getApplicationContext());
        button = (Button)findViewById(R.id.button);
        videoButton = (Button)findViewById(R.id.button2);
        textView = (TextView)findViewById(R.id.textView);
        textView2 = (TextView)findViewById(R.id.textView2);
        editText = (EditText)findViewById(R.id.editText);


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            if (ActivityCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                if (ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 100);
                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 100);
                    return;
                }
            }
        }
        enable_button();
        videoButton.setVisibility(View.INVISIBLE);
        videoButton.setOnClickListener((new View.OnClickListener(){
            @Override
            public void onClick(View view) {
                Intent myIntent;
                PackageManager manager = getPackageManager();
                myIntent = manager.getLaunchIntentForPackage("com.mxtech.videoplayer.ad");
                startActivity(myIntent);
            }
        })
        );
    }
    private void enable_button() {
        button.setOnClickListener((new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                textView.setText("please wait to upload file");
                new MaterialFilePicker()
                        .withActivity(MainActivity.this)
                        .withRequestCode(10)
                        .start();
            }
        }));
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        if (requestCode == 100 && (grantResults[0] == PackageManager.PERMISSION_GRANTED)){
            enable_button();
        }else {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
                requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 100);
                requestPermissions(new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 100);
            }
        }
    }

    private class  GetFileThread extends Thread{
        public void run() {
            try{
                System.out.println("getFileThread on");
                //Thread.sleep(5000);
                clientSocket = new Socket(serverIP, serverPort);
                networkWriter = new BufferedWriter(new OutputStreamWriter(clientSocket.getOutputStream()));
                networkReader = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

                networkWriter.write(f.getName() + '*' + editText.getText());
                networkWriter.flush();
                System.out.println("write");
                String file_name;

                file_name = networkReader.readLine();
                System.out.println(file_name);

                awsConnector.download(file_name);
            }
            catch(IOException e){
                e.printStackTrace();
            }
        }
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, final Intent data) {
        if (requestCode == 10 && resultCode == RESULT_OK) {
            f = new File(data.getStringExtra(FilePickerActivity.RESULT_FILE_PATH));
            String path = f.getPath();
            String file_path = f.getAbsolutePath();
            System.out.println(path);
            System.out.println(file_path);
            videoButton.setVisibility(View.VISIBLE);
            textView.setVisibility(View.INVISIBLE);
            textView2.setVisibility(View.INVISIBLE);
            button.setVisibility(View.INVISIBLE);
            editText.setVisibility(View.INVISIBLE);
            textView.setText("complete file uploading, Please Wait  ");
            awsConnector.upload(f);




            GetFileThread getFileThread = new GetFileThread();
            getFileThread.start();
            textView.setText("complete file download");

        }
    }
}

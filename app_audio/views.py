from django.shortcuts import render, redirect, HttpResponse
import pyaudio
import wave
from .models import Customer
from django.http import HttpResponseRedirect
import time
# Create your views here.
def show(req):
    return render(req, "form1.html")
def recordstart(req):

    try:
        global sample_format
        global chunk
        global channels
        global fs
        global frames
        chunk = 1024  # Record in chunks of 1024 samples
        sample_format = pyaudio.paInt16  # 16 bits per sample
        channels = 2
        fs = 44100  # Record at 44100 samples per second
        seconds = 3600
        global p
        p = pyaudio.PyAudio()  # Create an interface to PortAudio

        print('Recording')
        global stream
        stream = p.open(format=sample_format,
                        channels=channels,
                        rate=fs,
                        frames_per_buffer=chunk,
                        input=True)

        frames = []  # Initialize array to store frames

        # Store data in chunks for 30 seconds
        for i in range(0, int(fs / chunk * seconds)):
            data = stream.read(chunk)
            frames.append(data)
        message\
            =stream
    except OSError and ConnectionAbortedError:
          message="Record"
    return render(req, "form1.html", {"daa":message})
def recordstop(req):

    stream.stop_stream()
    message = "Recorded"
   # time.sleep(5)
    stream.close()
    # Terminate the PortAudio interface

    #p.terminate()
    time.sleep(100)
    print("Recording is stoped")

    return HttpResponseRedirect('/')
    #return render(req, "form1.html")
def recordsave(req):
    name=req.POST.get('name')
    y=str(name)+".mp3"
    print(name)
    print(y)
    filename = y
    
    # Save the recorded data as a WAV file
    wf = wave.open("app_audio/static/audio/"+filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    print("hii")
    wf.close()
    print("Recording is Saved")
    qs = Customer(audio=filename)
    qs.save()
    return render(req, "form1.html", {"d":filename})
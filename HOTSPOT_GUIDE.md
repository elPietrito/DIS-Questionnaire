# Hotspot Connection Guide for Local Connection

## Setup Steps

### Step 1: Enable Computer Hotspot
1. On your computer, go to Settings → Internet and Connections -> Personal Hotspot
2. Turn on the hotspot and connect with the tablet
3. Wait until connection is established, confirm the connection when a message of absence of Internet will appear

### Step 2: Enable python.exe on the Firewall connection and Streamlit 8051 from the advanced Firewall
1. Windows + R
2. Type "wf.msc"
3. In Inbound Rules -> activate Streamlit 8051 and python.exe rules
4. On windows Firewall settings, check the cases for private network for Python and python.exe

(If you need to create the Streamlit 8051 rule to open access to the 8051 port in a local network: Inbound Rules → New Rule, Port → Next, Specific local ports: 8501, Allow the connection, Name it: "Streamlit 8501")

### Step 3: Find Your Computer's IP Address
(If the program automatic detection does not work)

**On Windows:**
1. Open Command Prompt (cmd)
2. Type: `ipconfig`
3. Look for the section that says "Wireless LAN adapter Wi-Fi"
4. Find the line that says "IPv4 Address" 
5. The IP will look like: `192.168.xxx.xxx`
6. **This is your computer's IP address**

**Example:**
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.43.100
```
In this example, the IP is `192.168.43.100`

### Step 4: Run Streamlit with Network Access
1. Open Command Prompt in your project folder
2. Run this command:
   ```bash
   streamlit run app.py --server.address 0.0.0.0
   ```
3. **Important:** Use `0.0.0.0` to allow external connections!

### Step 5: Build Participant Link
1. Take your computer's IP from Step 3 (e.g., `192.168.43.100`)
2. Add `:8501/?participant=` and your participant ID
3. Full link example:
   ```
   http://192.168.43.100:8501/?participant=P001
   ```

### Step 6: Access on Phone/Tablet
1. On your phone, open a web browser (Chrome, Safari, etc.)
2. Type or paste the full link
3. The questionnaire should load!

## Common Issues & Solutions

### ❌ Problem: "Can't reach this page" or "Connection refused"

**Solution 1: Check Firewall**
Windows Firewall might be blocking Streamlit:
1. Go to Windows Settings → Privacy & Security → Windows Security → Firewall
2. Click "Allow an app through firewall"
3. Find "Python" or "Streamlit" 
4. Make sure both "Private" and "Public" boxes are checked
5. If not listed, click "Allow another app" and add Python

**Solution 2: Use Correct IP**
1. Make sure you're using the IP from `ipconfig`, not `localhost` or `127.0.0.1`
2. The IP should start with `192.168.` for phone hotspots
3. Expand the "Participant Link" section in the app - it shows your detected IP and ipconfig output

**Solution 3: Restart Streamlit with Network Flag**
Make absolutely sure you used:
```bash
streamlit run app.py --server.address 0.0.0.0
```

### ❌ Problem: Wrong IP Address Shown

The app now tries to auto-detect the correct IP, but if it's wrong:
1. Expand the "Participant Link" section
2. Look at the `ipconfig` output shown
3. Find your "Wireless LAN adapter" IPv4 address
4. Manually build the URL: `http://YOUR_IP:8501/?participant=YOUR_ID`

### ❌ Problem: Connection is Very Slow

Phone hotspots can be slower than WiFi:
1. Make sure you have good cellular signal
2. Try moving to a location with better reception
3. Consider using a regular WiFi router instead

### ❌ Problem: Port 8501 Already in Use

If you get an error about port 8501:
```bash
streamlit run app.py --server.address 0.0.0.0 --server.port 8502
```
Then use `:8502` instead of `:8501` in your URL

## Quick Test

To test if everything is working:

1. **On computer:** Run Streamlit
2. **On phone:** Open browser and go to `http://YOUR_COMPUTER_IP:8501`
3. You should see the Streamlit welcome page
4. If this works, add `/?participant=TEST` to access Part 2

## Alternative: Same Network Approach

If phone hotspot doesn't work, try this instead:

1. **Use a WiFi router** that both devices connect to
2. Connect computer to WiFi
3. Connect phone to the SAME WiFi
4. Find computer's IP with `ipconfig`
5. Use that IP in the participant link

## Still Not Working?

If none of the above works:

**Option 1: USB Tethering**
Some phones support USB tethering which is more reliable:
1. Connect phone to computer via USB
2. Enable USB tethering in phone settings
3. Computer will get internet through USB
4. Find the new IP with `ipconfig`

**Option 2: Local Testing**
For testing purposes only:
1. Click "👤 Start Local Debrief" button
2. Complete Part 2 on the same computer
3. This bypasses network issues entirely

**Option 3: Use Tablet/Computer on Same Network**
If you have a tablet or second computer:
1. Connect both to the same WiFi network
2. This avoids phone hotspot complications

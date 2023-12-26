#include <errno.h>
#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <termios.h>
#include <unistd.h>
#include <time.h>

#define MAX_SAMPLES 12 
//maximum samples for average should not be more than 12 so that every min
//there will be one param value sent to the server. P.S. this is for sample
//interval of 5 secs

int set_interface_attribs(int fd, int speed)
{
   struct termios tty;    if (tcgetattr(fd, &tty) < 0) {
       printf("Error from tcgetattr: %s\n", strerror(errno));
       return -1;
   }    cfsetospeed(&tty, (speed_t)speed);
   cfsetispeed(&tty, (speed_t)speed);    tty.c_cflag |= (CLOCAL | CREAD);    /* ignore modem controls */
   tty.c_cflag &= ~CSIZE;
   tty.c_cflag |= CS8;         /* 8-bit characters */
   tty.c_cflag &= ~PARENB;     /* no parity bit */
   tty.c_cflag &= ~CSTOPB;     /* only need 1 stop bit */
   tty.c_cflag &= ~CRTSCTS;    /* no hardware flowcontrol */    /* setup for non-canonical mode */
   tty.c_iflag &= ~(IGNBRK | BRKINT | PARMRK | ISTRIP | INLCR | IGNCR | ICRNL | IXON);
   tty.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);
   tty.c_oflag &= ~OPOST;    /* fetch bytes as they become available */
   tty.c_cc[VMIN] = 1;
   tty.c_cc[VTIME] = 1;    if (tcsetattr(fd, TCSANOW, &tty) != 0) {
       printf("Error from tcsetattr: %s\n", strerror(errno));
       return -1;
   }
   return 0;
}

void set_mincount(int fd, int mcount)
{
   struct termios tty;    if (tcgetattr(fd, &tty) < 0) {
       printf("Error tcgetattr: %s\n", strerror(errno));
       return;
   }    
   tty.c_cc[VMIN] = mcount ? 1 : 0;
   tty.c_cc[VTIME] = 5;        
   /* half second timer */    
   if (tcsetattr(fd, TCSANOW, &tty) < 0)
      printf("Error tcsetattr: %s\n", strerror(errno));
}
int main()
{

   char *portname = "/dev/ttyUSB1";
   int fd;
   int wlen;
   int recording_flag = 0;
   int response_index = 0;
   int response_length;
   unsigned char response[80];
   fd = open(portname, O_RDWR | O_NOCTTY | O_SYNC);
   if (fd < 0) {
       printf("Error opening %s: %s\n", portname, strerror(errno));
       return -1;
   }
   /*baudrate 115200, 8 bits, no parity, 1 stop bit*/
   set_interface_attribs(fd, 9600);
   //set_mincount(fd, 0);                /* set to pure timed read */    /* simple output */
   wlen = write(fd, "Hello!\n", 7);
   if (wlen != 7) {
       printf("Error from write: %d, %d\n", wlen, errno);
   }
   tcdrain(fd);    /* delay for output */    /* simple noncanonical input */
   int sample_number = 0;
   float sum_param = 0;
   response_index = 0;
   do {
       unsigned char buf[80];
       int rdlen;
       int number_of_samples = 6; //replace it with env value later
       rdlen = read(fd, buf, sizeof(buf) - 1);
       if (rdlen > 0) {
           unsigned char   *p;
	   p = buf; 
	   if(recording_flag == 1 || *p == '\x7d')
	   //start or end recording values
	   { 	
		recording_flag = 1;
		response[response_index] = *p;
		printf("all hex chars = 0x%x  --- %d\n", response[response_index],response_index);
		if(response_index > 1 && response[response_index-1] == '\x7d') //End of response
		{	
			response_length=response_index+1;
			recording_flag=0;
			response_index=0;
			printf("Command = 0x%x0x%x\n", response[8], response[9]);
			printf("Parameter Response = 0x%x%x%x%x\n", response[10], response[11], 
				response[12],response[13]);
			unsigned char uc[4];
			uc[3]=response[10];
			uc[2]=response[11];
			uc[1]=response[12];
			uc[0]=response[13];
			float f;
		
			memcpy(&f, uc, sizeof uc);
			printf("Parameter Value = %f\n", f);
			char str[420],str_display[200];

			sprintf(str, 
				"curl 'http://84.39.239.3:81/envirovis/device/rawdata_30min.php?value=%f&parameter=CO&company_id=AR&site_id=AR1003'",
				f);
	printf("%s\n", str);//main print statement
			system(str);
 			system(str_display);

			memset(response, 0, sizeof response);
			memset(uc, 0, sizeof uc);
			tcflush(fd, TCIOFLUSH);
		} else
		{
			response_index++;
		}
           }	
       } else if (rdlen < 0) {
           printf("Error from read: %d: %s\n", rdlen, strerror(errno));
       }
tcflush(fd, TCIOFLUSH);
       /* repeat read to get full message */
   } while (1);
}

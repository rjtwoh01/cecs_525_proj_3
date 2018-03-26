
 
#include <asf.h>
#include <stdio.h>
#include <comm.h>
#include <stdlib.h>
#include <ctype.h>


int z;
int last_temperaturec;
int last_temperaturef;
#define OUTPUT_STR_SIZE        32
char out_str[OUTPUT_STR_SIZE];
int critical;

static void adc_handler(ADC_t *adc, uint8_t ch_mask, adc_result_t result)
{
	#ifdef CONF_BOARD_OLED_UG_2832HSWEG04
	gfx_mono_draw_filled_rect(0,0,128,32,GFX_PIXEL_CLR);
	#endif
	int32_t temperature;
	char tx_buf[4] = {0, 0,0,0};
	uint8_t tx_length = 4;
	uint8_t i;
	int x;
	
	struct pwm_config mypwm[1]; //For your PWM configuration –CKH
	pwm_init(&mypwm[0], PWM_TCC0, PWM_CH_A, 1000);
	
	

	
	if (result > 697) {
		temperature = (int8_t)((-0.0295 * result) + 40.5);
	} if (result > 420) {
		temperature = (int8_t)((-0.0474 * result) + 53.3);
	} else {
		temperature = (int8_t)((-0.0777 * result) + 65.1);
	}

	last_temperaturec = temperature;
	last_temperaturef = (temperature*1.8)+32;
	
	
	
	

	if(last_temperaturef>critical)
	{
		x=100;
		pwm_start(&mypwm[0], x);
	}
	else
	{
		pwm_start(&mypwm[0], 0);
	}
	
	sprintf(tx_buf, "%d", last_temperaturef);
	for (i = 0; i < tx_length; i++) {
		usart_putchar(COMM, tx_buf[i]);
		
	}
	for (i = 0; i < tx_length; i++) {
		tx_buf[i]=0;
		
		
	}
	
	
	

		
	// Write temperature to display
	snprintf(out_str, OUTPUT_STR_SIZE, "Temperature: %4d C", last_temperaturec);
	gfx_mono_draw_string(out_str, 0, 0, &sysfont);
	
	snprintf(out_str, OUTPUT_STR_SIZE, "Temperature: %4d F", last_temperaturef);
	gfx_mono_draw_string(out_str, 0, 10, &sysfont);
	

	
	
}


int main(void)
{

	struct adc_config         adc_conf;
	struct adc_channel_config adcch_conf;
	

	board_init();
	sysclk_init();
	//sleepmgr_init();
	irq_initialize_vectors();
	cpu_irq_enable();
	gfx_mono_init();
	
	static usart_rs232_options_t USART_SERIAL_OPTIONS = {
		.baudrate = 9600,
		.charlength = (0x03<<0),
		.paritytype = (0x00<<4),
		.stopbits = true
	};
	usart_init_rs232(COMM, &USART_SERIAL_OPTIONS);
	
	
	// Enable backlight if display type is not OLED
	#ifndef CONF_BOARD_OLED_UG_2832HSWEG04
		ioport_set_pin_high(LCD_BACKLIGHT_ENABLE_PIN);
	#endif
	

	// Initialize configuration structures.
	adc_read_configuration(&ADCA, &adc_conf);
	adcch_read_configuration(&ADCA, ADC_CH0, &adcch_conf);

	/* Configure the ADC module:
	 * - unsigned, 12-bit results
	 * - VCC voltage reference
	 * - 200 kHz maximum clock rate
	 * - manual conversion triggering
	 * - temperature sensor enabled
	 * - callback function
	 */
	adc_set_conversion_parameters(&adc_conf, ADC_SIGN_ON, ADC_RES_12,
			ADC_REF_VCC);
	adc_set_clock_rate(&adc_conf, 200000UL);
	adc_set_conversion_trigger(&adc_conf, ADC_TRIG_MANUAL, 1, 0);
	adc_enable_internal_input(&adc_conf, ADC_INT_TEMPSENSE);

	adc_write_configuration(&ADCA, &adc_conf);
	adc_set_callback(&ADCA, &adc_handler);

	/* Configure ADC channel 0:
	 * - single-ended measurement from temperature sensor
	 * - interrupt flag set on completed conversion
	 * - interrupts disabled
	 */
	adcch_set_input(&adcch_conf, ADCCH_POS_PIN1, ADCCH_NEG_NONE,
			1);
	adcch_set_interrupt_mode(&adcch_conf, ADCCH_MODE_COMPLETE);
	adcch_enable_interrupt(&adcch_conf);

	adcch_write_configuration(&ADCA, ADC_CH0, &adcch_conf);

	// Enable the ADC and start the first conversion.
	adc_enable(&ADCA);
	adc_start_conversion(&ADCA, ADC_CH0);
	

	
	do {		
		//uint8_t tx_length = 4;
		//uint8_t i;
		
		if (usart_rx_is_complete(COMM) == true)
		{	//for (i = 0; i < tx_length; i++) 
			//{
			uint8_t received_byte = usart_getchar(COMM);
			critical=(int)received_byte;
			
			//}
			
			snprintf(out_str, OUTPUT_STR_SIZE, "Critical Temp: %d ", received_byte);
			gfx_mono_draw_string(out_str, 0, 20, &sysfont);
		}
		
		
		
		adc_start_conversion(&ADCA, ADC_CH0);

		/*received_byte=usart_getchar(COMM);
		snprintf(out_str, OUTPUT_STR_SIZE, "Critical Temp: %4d ", received_byte);
		gfx_mono_draw_string(out_str, 0, 20, &sysfont);
		usart_putchar(COMM,received_byte);*/
	} while (1);
	
}


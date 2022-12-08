/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include <stdio.h>
#include <string.h>
#include <stdbool.h>
#include <math.h>
#include <stdlib.h>

/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
ADC_HandleTypeDef hadc1;
DMA_HandleTypeDef hdma_adc1;

TIM_HandleTypeDef htim1;

UART_HandleTypeDef huart6;
DMA_HandleTypeDef hdma_usart6_rx;

/* USER CODE BEGIN PV */

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
static void MX_GPIO_Init(void);
static void MX_DMA_Init(void);
static void MX_ADC1_Init(void);
static void MX_USART6_UART_Init(void);
static void MX_TIM1_Init(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */
uint16_t adcValArray [3];    //array of 3 elements because I activated only 3 ADC channels. every channel has one sensor reading.
uint16_t voltage_sensor1;
uint16_t voltage_sensor2;
int current_sensor1;
float output_voltage;
float current , true_read_digital_current;
float voltage;
uint16_t digital_read_internal_temp_sensor;

float internal_temp_sensor;
bool flag = false;

uint16_t battery_temperature;
char rxdata [6];
float  Cell1_State_of_charge;
int Cell1_State_of_health;
/*******************Start setup code of DHT22*************************/
#define DHT22_PORT GPIOB
#define DHT22_PIN GPIO_PIN_9
uint8_t RH1, RH2, TC1, TC2, SUM, CHECK;
uint32_t pMillis, cMillis;
float tCelsius = 0;
float tFahrenheit = 0;
float RH = 0;

void microDelay (uint16_t delay)
{
  __HAL_TIM_SET_COUNTER(&htim1, 0);
  while (__HAL_TIM_GET_COUNTER(&htim1) < delay);
}

uint8_t DHT22_Start (void)
{
  uint8_t Response = 0;
  GPIO_InitTypeDef GPIO_InitStructPrivate = {0};
  GPIO_InitStructPrivate.Pin = DHT22_PIN;
  GPIO_InitStructPrivate.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStructPrivate.Speed = GPIO_SPEED_FREQ_LOW;
  GPIO_InitStructPrivate.Pull = GPIO_NOPULL;
  HAL_GPIO_Init(DHT22_PORT, &GPIO_InitStructPrivate); // set the pin as output
  HAL_GPIO_WritePin (DHT22_PORT, DHT22_PIN, 0);   // pull the pin low
  microDelay (1300);   // wait for 1300us
  HAL_GPIO_WritePin (DHT22_PORT, DHT22_PIN, 1);   // pull the pin high
  microDelay (30);   // wait for 30us
  GPIO_InitStructPrivate.Mode = GPIO_MODE_INPUT;
  GPIO_InitStructPrivate.Pull = GPIO_PULLUP;
  HAL_GPIO_Init(DHT22_PORT, &GPIO_InitStructPrivate); // set the pin as input
  microDelay (40);
  if (!(HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN)))
  {
    microDelay (80);
    if ((HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN))) Response = 1;
  }
  pMillis = HAL_GetTick();
  cMillis = HAL_GetTick();
  while ((HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN)) && pMillis + 2 > cMillis)
  {
    cMillis = HAL_GetTick();
  }
  return Response;
}

uint8_t DHT22_Read (void)
{
  uint8_t a,b;
  for (a=0;a<8;a++)
  {
    pMillis = HAL_GetTick();
    cMillis = HAL_GetTick();
    while (!(HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN)) && pMillis + 2 > cMillis)
    {  // wait for the pin to go high
      cMillis = HAL_GetTick();
    }
    microDelay (40);   // wait for 40 us
    if (!(HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN)))   // if the pin is low
      b&= ~(1<<(7-a));
    else
      b|= (1<<(7-a));
    pMillis = HAL_GetTick();
    cMillis = HAL_GetTick();
    while ((HAL_GPIO_ReadPin (DHT22_PORT, DHT22_PIN)) && pMillis + 2 > cMillis)
    {  // wait for the pin to go low
      cMillis = HAL_GetTick();
    }
  }
  return b;
}
/*******************End setup code of DHT22*************************/

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_USART6_UART_Init();
  MX_TIM1_Init();
  /* USER CODE BEGIN 2 */
  /************* Start the code of start the ADC conversion process*****************/
  HAL_ADC_Start_DMA(&hadc1,(uint32_t *) adcValArray,3);
  /************* End the code of start the ADC conversion process*****************/
  /************* Start the code of start timer_1 for DHT22 *****************/
  HAL_TIM_Base_Start(&htim1);
  /************* End the code of start timer_1 for DHT22 *****************/

  /************* Start the code of UART receive *****************/
 //************* Start the code of UART receive *****************/
  HAL_UART_Receive_DMA (&huart6,(uint8_t *) rxdata,sizeof(rxdata));
  	 //soc = atoi (rxdata);
 //************* End the code of UART receive *****************/

  /************* Start the code of get the temperature sensor reading*****************/
uint16_t get_temperature_sensor ()
{
	if(DHT22_Start())
	    {
	      RH1 = DHT22_Read(); // First 8bits of humidity
	      RH2 = DHT22_Read(); // Second 8bits of Relative humidity
	      TC1 = DHT22_Read(); // First 8bits of Celsius
	      TC2 = DHT22_Read(); // Second 8bits of Celsius
	      SUM = DHT22_Read(); // Check sum
	      CHECK = RH1 + RH2 + TC1 + TC2;
	      if (CHECK == SUM)
	      {
	        if (TC1>127) // If TC1=10000000, negative temp rature
	        {
	          tCelsius = (float)TC2/10*(-1);
	        }
	        else
	        {
	          tCelsius = (float)((TC1<<8)|TC2)/10;
	        }
	        tFahrenheit = tCelsius * 9/5 + 32;
	        RH = (float) ((RH1<<8)|RH2)/10;
	      }
	    }
	  HAL_Delay(1000);
	  uint16_t trmperature_celsius = (uint16_t) (tCelsius*10);
	  return trmperature_celsius;

}
  /************* End the code of get the temperature sensor reading*****************/

  /************* Start the code of get the current sensor reading*****************/
int  current_sensor ()
 {
	 const uint16_t samples = 10;
	 int ADC_error = 371;
	 float current_sensor_sensitivity = 0.4;                // from the data sheet of current sensor the sensitivity = 400 mV/A.
	 uint16_t read_digital_current;
	 /*****for loop to get the average value of the sensor output, to increase the accuracy.***/
	 for (int i = 0; i < samples; i++)
	   {

		 read_digital_current += (adcValArray [0] - ADC_error);
	     HAL_Delay(10);                         // wait 10 milliseconds before the next loop.
	   }
      /******** End for loop******************************/
	 true_read_digital_current = read_digital_current / samples;
	 output_voltage = (float) true_read_digital_current*3.3/ 4095;
	 read_digital_current = 0;                        // Initialize the reading value to zero for the next process.

	 current =(output_voltage - 2.364)/current_sensor_sensitivity ;          // 2.5 at Vcc= 5 V and temperature = 25° C .
	 if( current <= 0.02 && current >= -0.01)
	 {
		 current = 0;
	 }

	 int current_to_send = (int) (1000*current);



	 return current_to_send;
  }




 /*int  current_sensor (uint16_t read_digital_current)
 {
	 float current_sensor_error;
	 float current_sens_sensitivity = 0.066;
	 output_voltage = (float) read_digital_current*3.3*2/ 4095;
	     // calibration the current sensor  accuracy.
	 /*if (internal_temp_sensor >= -25  && internal_temp_sensor < 25){
		 current_sensor_error = -0.004 *internal_temp_sensor + 0.3;
	 }
	 else if (internal_temp_sensor >= 25 && internal_temp_sensor < 85){
		 current_sensor_error = 0.01 *internal_temp_sensor + 0.05;
	 }*/

	 /*float true_output_voltage= output_voltage * (1-0.2);    //0.2 is the current_sensor_error.
	 current =(true_output_voltage - 2.5)/current_sens_sensitivity ;  // from the data sheet of current sensor in case of Ip=30, the sensitivity = 66 mV/A.

	 int current_to_send = (int) (1000*current)/20;  // (20)only to calibrate the value (it should be changed)


     return current_to_send;
  }*/
 /************* End the code of get the current sensor reading*****************/

 uint16_t  voltage_sensor (uint16_t read_digital_voltage)
  {
 	 float ADC_error = 0.89;
 	 float voltage_sens_sensitivity = 0.2;
 	 uint16_t true_digital_voltage = read_digital_voltage;
 	 voltage = (float) 1000*true_digital_voltage *3.3/voltage_sens_sensitivity*ADC_error/4095;
 	 uint16_t voltageToSend = (uint16_t) voltage;
 	 /*if (voltageToSend > 1500)
 	 {
 		voltageToSend = 1500;
 	 }*/

     return voltageToSend;
   }
 /****************************************************/
 void uart_uint16_transmit (char ID, uint16_t data_to_send)
 {

	 char  txdata [35];
	 sprintf(txdata, "%c%u \r\n", ID,data_to_send);
	 HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
	 //HAL_Delay(500);
   }
/*************************************************************/
 void uart_current_transmit (char ID, int data_to_send)
  {

 	 char  txdata [35];
 	 sprintf(txdata, "%c%d \r\n", ID,data_to_send);
 	 HAL_UART_Transmit(&huart6,(uint8_t *) txdata, strlen(txdata), 10);
 	 //HAL_Delay(500);
    }
 /***********************************************************/

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */


	  /********* Start code of reading the internal temperature sensor to adjust the output voltage of the current sensor*************/
	  digital_read_internal_temp_sensor = adcValArray [2];
	  float Vout_internal_temp_sensor = (float) digital_read_internal_temp_sensor*3.3/4095;
	  float error = 0.081;
	  internal_temp_sensor = (Vout_internal_temp_sensor- error - 0.76) / 0.0025 + 25;               // 0.76
	  /********* End code of reading the internal temperature sensor to adjust the output voltage of the current sensor*************/

	  /*if (flag == false){
	  		  HAL_Delay(5000);                       // wait for 5 seconds to let the ADC get the true right value
	  		  flag= true;
	  	  }*/

	  //current_sensor1 = current_sensor (adcValArray [0]);
	  current_sensor1 = current_sensor ();
	  voltage_sensor1 = voltage_sensor (adcValArray [1]);
	  battery_temperature = get_temperature_sensor ();


	  uart_uint16_transmit ('a',voltage_sensor1);
	  HAL_Delay(1000);

	  uart_uint16_transmit ('t',battery_temperature);
	  	  HAL_Delay(1000);

	 // uart_voltage_transmit ('b',voltage_sensor2);
	  //HAL_Delay(1000);

	  uart_current_transmit ('i',current_sensor1);
	  HAL_Delay(1000);





  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  __HAL_RCC_PWR_CLK_ENABLE();
  __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE1);

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_NONE;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_HSI;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV2;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_0) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief ADC1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_ADC1_Init(void)
{

  /* USER CODE BEGIN ADC1_Init 0 */

  /* USER CODE END ADC1_Init 0 */

  ADC_ChannelConfTypeDef sConfig = {0};

  /* USER CODE BEGIN ADC1_Init 1 */

  /* USER CODE END ADC1_Init 1 */

  /** Configure the global features of the ADC (Clock, Resolution, Data Alignment and number of conversion)
  */
  hadc1.Instance = ADC1;
  hadc1.Init.ClockPrescaler = ADC_CLOCK_SYNC_PCLK_DIV8;
  hadc1.Init.Resolution = ADC_RESOLUTION_12B;
  hadc1.Init.ScanConvMode = ENABLE;
  hadc1.Init.ContinuousConvMode = ENABLE;
  hadc1.Init.DiscontinuousConvMode = DISABLE;
  hadc1.Init.ExternalTrigConvEdge = ADC_EXTERNALTRIGCONVEDGE_NONE;
  hadc1.Init.ExternalTrigConv = ADC_SOFTWARE_START;
  hadc1.Init.DataAlign = ADC_DATAALIGN_RIGHT;
  hadc1.Init.NbrOfConversion = 3;
  hadc1.Init.DMAContinuousRequests = ENABLE;
  hadc1.Init.EOCSelection = ADC_EOC_SINGLE_CONV;
  if (HAL_ADC_Init(&hadc1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_7;
  sConfig.Rank = 1;
  sConfig.SamplingTime = ADC_SAMPLETIME_480CYCLES;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_8;
  sConfig.Rank = 2;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }

  /** Configure for the selected ADC regular channel its corresponding rank in the sequencer and its sample time.
  */
  sConfig.Channel = ADC_CHANNEL_TEMPSENSOR;
  sConfig.Rank = 3;
  if (HAL_ADC_ConfigChannel(&hadc1, &sConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN ADC1_Init 2 */

  /* USER CODE END ADC1_Init 2 */

}

/**
  * @brief TIM1 Initialization Function
  * @param None
  * @retval None
  */
static void MX_TIM1_Init(void)
{

  /* USER CODE BEGIN TIM1_Init 0 */

  /* USER CODE END TIM1_Init 0 */

  TIM_ClockConfigTypeDef sClockSourceConfig = {0};
  TIM_MasterConfigTypeDef sMasterConfig = {0};

  /* USER CODE BEGIN TIM1_Init 1 */

  /* USER CODE END TIM1_Init 1 */
  htim1.Instance = TIM1;
  htim1.Init.Prescaler = 11;
  htim1.Init.CounterMode = TIM_COUNTERMODE_UP;
  htim1.Init.Period = 65535;
  htim1.Init.ClockDivision = TIM_CLOCKDIVISION_DIV1;
  htim1.Init.RepetitionCounter = 0;
  htim1.Init.AutoReloadPreload = TIM_AUTORELOAD_PRELOAD_DISABLE;
  if (HAL_TIM_Base_Init(&htim1) != HAL_OK)
  {
    Error_Handler();
  }
  sClockSourceConfig.ClockSource = TIM_CLOCKSOURCE_INTERNAL;
  if (HAL_TIM_ConfigClockSource(&htim1, &sClockSourceConfig) != HAL_OK)
  {
    Error_Handler();
  }
  sMasterConfig.MasterOutputTrigger = TIM_TRGO_RESET;
  sMasterConfig.MasterSlaveMode = TIM_MASTERSLAVEMODE_DISABLE;
  if (HAL_TIMEx_MasterConfigSynchronization(&htim1, &sMasterConfig) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN TIM1_Init 2 */

  /* USER CODE END TIM1_Init 2 */

}

/**
  * @brief USART6 Initialization Function
  * @param None
  * @retval None
  */
static void MX_USART6_UART_Init(void)
{

  /* USER CODE BEGIN USART6_Init 0 */

  /* USER CODE END USART6_Init 0 */

  /* USER CODE BEGIN USART6_Init 1 */

  /* USER CODE END USART6_Init 1 */
  huart6.Instance = USART6;
  huart6.Init.BaudRate = 115200;
  huart6.Init.WordLength = UART_WORDLENGTH_8B;
  huart6.Init.StopBits = UART_STOPBITS_1;
  huart6.Init.Parity = UART_PARITY_NONE;
  huart6.Init.Mode = UART_MODE_TX_RX;
  huart6.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart6.Init.OverSampling = UART_OVERSAMPLING_16;
  if (HAL_UART_Init(&huart6) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART6_Init 2 */

  /* USER CODE END USART6_Init 2 */

}

/**
  * Enable DMA controller clock
  */
static void MX_DMA_Init(void)
{

  /* DMA controller clock enable */
  __HAL_RCC_DMA2_CLK_ENABLE();

  /* DMA interrupt init */
  /* DMA2_Stream0_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream0_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream0_IRQn);
  /* DMA2_Stream1_IRQn interrupt configuration */
  HAL_NVIC_SetPriority(DMA2_Stream1_IRQn, 0, 0);
  HAL_NVIC_EnableIRQ(DMA2_Stream1_IRQn);

}

/**
  * @brief GPIO Initialization Function
  * @param None
  * @retval None
  */
static void MX_GPIO_Init(void)
{
  GPIO_InitTypeDef GPIO_InitStruct = {0};

  /* GPIO Ports Clock Enable */
  __HAL_RCC_GPIOH_CLK_ENABLE();
  __HAL_RCC_GPIOA_CLK_ENABLE();
  __HAL_RCC_GPIOB_CLK_ENABLE();
  __HAL_RCC_GPIOC_CLK_ENABLE();

  /*Configure GPIO pin Output Level */
  HAL_GPIO_WritePin(GPIOB, GPIO_PIN_9, GPIO_PIN_RESET);

  /*Configure GPIO pin : PB9 */
  GPIO_InitStruct.Pin = GPIO_PIN_9;
  GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
  GPIO_InitStruct.Pull = GPIO_NOPULL;
  GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
  HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

}

/* USER CODE BEGIN 4 */
/********** Start of UART receive callback function***************/
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart)
{
  /* Prevent unused argument(s) compilation warning */
  UNUSED(huart);
  /* NOTE: This function should not be modified, when the callback is needed,
           the HAL_UART_RxCpltCallback could be implemented in the user file
   */
  if (rxdata[0] == 's')
  {
	  rxdata[0]=' ';
	  char cell1_soc [6];
	  sprintf(cell1_soc,"%s",rxdata);
	  Cell1_State_of_charge = atof (cell1_soc);
	  //Cell1_State_of_charge = round(Cell1_State_of_charge*100) / 100;
	  //float socf = (float) soc/100.00;
	  //Cell1_State_of_charge = soc/100;
  }
  else if (rxdata[0] == 'h')
    {
  	  rxdata[0]=' ';
  	  char cell1_soh [6];
  	  sprintf(cell1_soh,"%s",rxdata);
  	  Cell1_State_of_health = (atoi (cell1_soh))/1000;

    }
  else if (rxdata[0] == 'e')
  {
	  rxdata[0]=' ';
	  char error [6];
	  sprintf(error,"%s",rxdata);
	  int int_error = atoi (error);
	  if (int_error == 1){
		  printf("make sure the current sensor_1 is connected!");
	  }
	  else if (int_error == 5){
		  printf("Please, replace the cell_1 with a new one!");
	  }
  }

}
/********** End of UART receive callback function***************/
/**********Start of  Check the ID of the sensor reading, then convert it to the true value without the ID (the ID is the first char).**************/
/*switch (rxdata[0]) {   //check the ID of the received data, then convert it to the true value without the ID (the ID is the first char).
          case 's':
              {
            	  rxdata[0]=' ';
                  char cell1_soc [4];
                  sprintf(cell1_soc,"%s",rxdata);
                  int soc = atoi (cell1_soc);
                  float socf = (float) soc/100;
                  Cell1_State_of_charge = roundf(socf*100) / 100;
              }
              break;
          /*default:
                      // if frist charackter doesn't match any case )

                      //do something;
                      break;*/
/********** End of  Check the ID of the sensor reading, then convert it to the true value without the ID (the ID is the first char).**************/
/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

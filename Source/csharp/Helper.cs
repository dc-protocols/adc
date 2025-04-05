/*
Copyright (c) 2010, ADCProject
All rights reserved.
    
Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of the ADCProject nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL ADCProject BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
*/

using System;
using System.Collections.Generic;
using System.Text;
using System.Text.RegularExpressions;

namespace ADC
{
    public class Helper
    {
        /// <summary>
        /// Escapes an ADC string.
        /// </summary>
        /// <param name="strInitial">The input string value.</param>
        /// <returns>The escaped string value.</returns>
        public static string Escape(string strInput)
        {
            string strOutput = strInput;

            // Escape backslash
            strOutput = strOutput.Replace("\\", "\\\\");

            // Escape tab
            strOutput = strOutput.Replace("\t", "\\t");

            // Escape space
            Regex regex = new Regex(@"[ ]{1,}", RegexOptions.None);
            strOutput = regex.Replace(strOutput, @"\s");

            return strOutput;
        }

        //public static string UnEscape(string strInput)
        //{
        //    string strOutput = strInput;

        //    strOutput = strOutput.Replace("\\t", "\t");

        //    strOutput = strOutput.Replace("\\\\", "\\");

            


        //}
    }
}
